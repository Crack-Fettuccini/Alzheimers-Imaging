import numpy as np
import matplotlib.pyplot as plt
from nilearn import plotting
import nibabel as nib
from skimage.transform import resize
from matplotlib.animation import FuncAnimation

mri_img = nib.load("/Users/admin/Desktop/Alzheimer's/ADNI/011_S_6303/Axial_T2_STAR/2018-04-12_13_06_54.0/output.nii.gz")
pet_img = nib.load("/Users/admin/Desktop/Alzheimer's/ADNI/011_S_6303/ADNI3_FDG__AC_/2018-05-04_14_26_26.0/output.nii.gz")

# Get the data arrays from the images
mri_data = mri_img.get_fdata()
pet_data = pet_img.get_fdata()
pet_data_resized = resize(pet_data, mri_data.shape, mode='constant')

# Normalize the intensity values of both images
mri_data_norm = (mri_data - np.min(mri_data)) / (np.max(mri_data) - np.min(mri_data))
pet_data_norm = (pet_data_resized - np.min(pet_data_resized)) / (np.max(pet_data_resized) - np.min(pet_data_resized))

# Superimpose the two images by blending them
blended_data = 0.5 * mri_data_norm + 0.5 * pet_data_norm

# Create a new NIfTI image with the blended data
blended_img = nib.Nifti1Image(blended_data, affine=mri_img.affine)

# Define the slice indices
mri_shape = mri_img.shape
slice_indices = np.linspace(0, mri_shape[2] - 1, 9, dtype=int)

# Create the figure and axes
fig, axes = plt.subplots(3, 1)

# Function to update the plot with the next slice
def update(frame):
    axes[0].cla()
    axes[1].cla()
    axes[2].cla()
    plotting.plot_epi(blended_img, display_mode='z', draw_cross=True, title='Superimposed Images', axes=axes[0], cut_coords=[frame])
    plotting.plot_epi(mri_img, display_mode='z', draw_cross=True, title='MRI', axes=axes[1], cut_coords=[frame])
    plotting.plot_epi(pet_img, display_mode='z', draw_cross=True, title='PET', axes=axes[2], cut_coords=[frame])
    plt.tight_layout(pad=0)

# Create the animation
ani = FuncAnimation(fig, update, frames=slice_indices, interval=1000)  # Update every 1 second
plt.tight_layout(pad=0)

plt.show()
