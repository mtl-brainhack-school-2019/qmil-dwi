import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from dipy.core.gradients import gradient_table
import dipy.reconst.dki as dki
import dipy.reconst.dti as dti
from dipy.segment.mask import median_otsu
from scipy.ndimage.filters import gaussian_filter
from dipy.reconst.dti import fractional_anisotropy, color_fa


# PRE-PROCESSING

# set input data file path
data_dir = 'D:\\McGill\\Rotation1\\CPZ_3WK_BrainA\\'
b0dir = os.path.join(data_dir, 'b0img.nii')             # b0 image (N = 6)
b1dir = os.path.join(data_dir, 'b2500img.nii')          # 1st b-value image (N = 30)
b2dir = os.path.join(data_dir, 'b4000img.nii')          # 2nd b-value image (N = 60)
images = [b0dir, b1dir, b2dir]

bval = np.loadtxt(os.path.join(data_dir, 'bval_all.txt')) # b values
bvec = np.loadtxt(os.path.join(data_dir, 'bvec_all.txt')) # b directions
bvec = np.reshape(bvec, (len(images), len(bval)))

# load 4D image data
imgb0 = nib.load(images[0])
imgb0dat = imgb0.get_data()
imgb1 = nib.load(images[1])
imgb1dat = imgb1.get_data()
imgb2 = nib.load(images[2])
imgb2dat = imgb2.get_data()
affine = imgb0.affine

# concatenate
imgcatdat = np.squeeze(np.concatenate((imgb0dat[..., None], imgb1dat[..., None], imgb2dat[..., None]), axis=3))

# prepare mask to remove background
maskdat, mask = median_otsu(imgcatdat, vol_idx=range(35, 95), median_radius=2, numpass=1)

# apply gaussian smoothing to suppress artefacts and noise
fwhm = 1.25
gauss_std = fwhm / np.sqrt(8 * np.log(2))  # converting fwhm to Gaussian std
imgready = np.zeros(maskdat.shape)
for v in range(maskdat.shape[-1]):
    imgready[..., v] = gaussian_filter(maskdat[..., v], sigma=gauss_std)

# FIT DTI AND KTI MODELS

gtab = gradient_table(bval, bvec)

# diffusion tensor
print('Computing DTI parameters')
tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(imgready)
dti_FA = tenfit.fa
dti_MD = tenfit.md
dti_AD = tenfit.ad
dti_RD = tenfit.rd

# kurtosis tensor
print('Computing DKI parameters')
dkimodel = dki.DiffusionKurtosisModel(gtab)
dkifit = dkimodel.fit(imgready)
FA = dkifit.fa
MD = dkifit.md
AD = dkifit.ad
RD = dkifit.rd

# generate plots

axslice = 42

fig1, ax = plt.subplots(2, 4, figsize=(12, 6), subplot_kw={'xticks': [], 'yticks': []})
fig1.subplots_adjust(hspace=0.3, wspace=0.05)

ax.flat[0].imshow(FA[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[0].set_title('FA (DKI)')
ax.flat[1].imshow(MD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[1].set_title('MD (DKI)')
ax.flat[2].imshow(AD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[2].set_title('AD (DKI)')
ax.flat[3].imshow(RD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[3].set_title('RD (DKI)')

ax.flat[4].imshow(dti_FA[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[4].set_title('FA (DTI)')
ax.flat[5].imshow(dti_MD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[5].set_title('MD (DTI)')
ax.flat[6].imshow(dti_AD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[6].set_title('AD (DTI)')
ax.flat[7].imshow(dti_RD[:, :, axslice].T, cmap='gray', origin='lower')
ax.flat[7].set_title('RD (DTI)')

plt.show()
fig1.savefig('Diffusion_tensor_measures_from_DTI_and_DKI.png')



# save RGB for later use

dti_FA[np.isnan(dti_FA)] = 0
RGB = np.clip(dti_FA, 0, 1)
RGB = color_fa(RGB, tenfit.evecs)

nib.save(nib.Nifti1Image(np.array(255 * RGB, 'uint8'), affine), os.path.join(data_dir, 'tensor_rgb.nii.gz'))





