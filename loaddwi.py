import os
import numpy as np
import nibabel as nib

from dipy.core.gradients import gradient_table
from dipy.reconst.dti import TensorModel
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

# load 4D image data, concatenate, create new .nii
imgb0 = nib.load(images[0])
imgb0dat = imgb0.get_fdata()
imgb1 = nib.load(images[1])
imgb1dat = imgb1.get_fdata()
imgb2 = nib.load(images[2])
imgb2dat = imgb2.get_fdata()

imgcatdat = np.concatenate((imgb0dat[..., None], imgb1dat[..., None], imgb2dat[..., None]), axis=3)
imgcatdat = np.squeeze(imgcatdat)

imgcat = nib.Nifti1Image(imgcatdat, imgb0.affine)
# nib.save(imgcat, os.path.join(data_dir,'imgcat.nii'))

# FIT DTI


gtab = gradient_table(bval, bvec)
tenmodel = TensorModel(gtab)
tenfit = tenmodel.fit(imgcatdat)

# compute fractional anisotropy
print('Computing anisotropy measures (FA, MD, RGB)')

FA = fractional_anisotropy(tenfit.evals)
FA[np.isnan(FA)] = 0

fa_img = nib.Nifti1Image(FA.astype(np.float32), imgb0.affine)

FA = np.clip(FA, 0, 1)
RGB = color_fa(FA, tenfit.evecs)

nib.save(fa_img, os.path.join(data_dir, 'tensor_fa.nii.gz'))
nib.save(nib.Nifti1Image(np.array(255 * RGB, 'uint8'), imgb0.affine), os.path.join(data_dir, 'tensor_rgb.nii.gz'))




