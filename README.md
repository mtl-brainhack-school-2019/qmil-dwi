Quantitative Microstructure Imaging Laboratory - Diffusion Weighted MRI
=============

Vladimir Grouza

Supervisor: Dr. David Rudko

Rotation project: use diffusion MR parameter metrics to quantify demyelination in mice on a persistent diet of cuprizone (CPZ). For the purpose of the Brainhack school, I aim to make use of open source tools to implement a small pipeline to import and manipulate image data in a python environment and attempt to familarize myself with the diffusion map fitting process. 

## Data Set ##

Each complete acquisition yeilds a b_0 image, a set of images at at leasat two feild strengths, and a gradient table. These are required to fit a diffusion tensor.

- [x] a single animal
- [ ] approximately 20 animals: vehicle, 3-week CPZ, 5-week CPZ 

## Preprocessing ## 
- [x] Reconstruct raw data (done a priori)
- [x] Import .nii files into a python environment
- [x] Concatenate volumetric data 
- [x] Perform segmentation to remove non-brain background (masking)
- [x] Apply a gaussian filter to suppress noise and smooth discontinuities



![picture alt](https://github.com/mtl-brainhack-school-2019/qmil-dwi/blob/master/axial_Diffusion_tensor_measures_from_DTI_and_DKI.png "Title is optional")
