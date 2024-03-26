import os
import pydicom
import numpy as np
import nibabel as nib
import xml.etree.ElementTree as ET

def parse_xml_metadata(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract relevant metadata from XML
    pixel_spacing_x = float(root.find(".//protocol[@term='Pixel Spacing X']").text)
    pixel_spacing_y = float(root.find(".//protocol[@term='Pixel Spacing Y']").text)
    slice_thickness = float(root.find(".//protocol[@term='Slice Thickness']").text)
    matrix_x = int(float(root.find(".//protocol[@term='Matrix X']").text))
    matrix_y = int(float(root.find(".//protocol[@term='Matrix Y']").text))
    matrix_z = int(float(root.find(".//protocol[@term='Matrix Z']").text))
    field_strength = float(root.find(".//protocol[@term='Field Strength']").text)
    
    return (pixel_spacing_x, pixel_spacing_y), slice_thickness, (matrix_x, matrix_y, matrix_z), field_strength


def convert_dicom_to_nifti(dicom_dir, output_file, pixel_spacing, slice_thickness, matrix_size):
    dicom_files = [os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.endswith('.dcm')]
    dicom_files.sort()  # Sort files to ensure correct order
    dicom_slices = [pydicom.dcmread(f) for f in dicom_files]
    
    pixel_data = np.stack([d.pixel_array for d in dicom_slices], axis=-1)
    
    nifti_img = nib.Nifti1Image(pixel_data, affine=np.eye(4))
    nifti_img.header.set_zooms(pixel_spacing + (slice_thickness,))
    nifti_img.header.set_xyzt_units('mm', 'sec')
    nifti_img.header['qform_code'] = 1
    nifti_img.header['sform_code'] = 1
    nifti_img.header['srow_x'] = [pixel_spacing[0], 0, 0, 0]
    nifti_img.header['srow_y'] = [0, pixel_spacing[1], 0, 0]
    nifti_img.header['srow_z'] = [0, 0, slice_thickness, 0]
    
    # Save NIfTI image
    nib.save(nifti_img, output_file)

# Path to the XML file containing metadata
xml_file = "/Users/admin/Desktop/Alzheimer's/ADNI/011_S_6303/ADNI/ADNI_011_S_6303_Axial_T2_STAR_S676287_I985200.xml"

# Call parse_xml_metadata function to extract metadata
pixel_spacing, slice_thickness, matrix_size, field_strength = parse_xml_metadata(xml_file)

# Path to the directory containing DICOM files
dicom_directory = "/Users/admin/Desktop/Alzheimer's/ADNI/011_S_6303/Axial_T2_STAR/2018-04-12_13_06_54.0/I985200"

# Path to the output NIfTI file
output_nifti_file = "/Users/admin/Desktop/Alzheimer's/ADNI/011_S_6303/Axial_T2_STAR/2018-04-12_13_06_54.0/output.nii.gz"

# Convert DICOM to NIfTI using extracted metadata
convert_dicom_to_nifti(dicom_directory, output_nifti_file, pixel_spacing, slice_thickness, matrix_size)
