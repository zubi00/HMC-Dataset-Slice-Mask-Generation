# HMC-Dataset-Slice-Mask-Generation

We have collected a Head & Neck cancer patient dataset from Hamad Medical Corporation (HMC) Hospital. While the dataset is not publicly available, the following steps outline the preprocessing methodology to help you better understand how hospital datasets can be organized and utilized effectively:

1. Install Dependencies:

   Ensure all required dependencies and libraries are installed.


2. Clone the Repository:

   Clone this repository to your local machine and extract the files.



3. Steps for Preprocessing:

   Below are the functionalities provided by the scripts included in the repository:


   i. FileOrganize.py:

       This script organizes DICOM files for each patient by creating separate folders, such as CT, MRI, PET, RTDOSE, RTIMAGE, RTPLAN, and MASK. Additionally, it creates subfolders within CT, MRI, and PET directories based on the series description for better organization.


   ii. RSFile.py:

       This script iterates through the subfolders of each patient directory to locate the structure files (RS files) and copies them into the corresponding CT DICOM imaging folder.


    iii. DICOM2NIfTI.py:

         This script converts DICOM imaging data into NIfTI format, generating slices and corresponding colored masks for different anatomical structures.



     iv. NIfTI2PNG&Masks.py:

         This script converts NIfTI files into PNG images of slices and their respective masks.

   

Feel free to reach out to me for assistance or further clarification at zubairsaeed602@gmail.com.
