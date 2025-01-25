import osimport nibabel as nibimport numpy as npfrom PIL import Imageimport randomdef nifti_to_png_slices_and_masks(nifti_root_folder, output_root_folder, structures_of_interest):    color_map = {        'GTV1': [255, 0, 0],        # Red        'Spinal Cord': [0, 255, 0], # Green        'Rt Parotid': [0, 0, 255],  # Blue        'Lt Parotid': [255, 255, 0],# Yellow        'Mandible': [255, 0, 255],  # Magenta        'Rt Eye': [0, 255, 255],    # Cyan        'Lt Eye': [128, 0, 0],      # Maroon        'Rt Optic Nerve': [0, 128, 0], # Dark Green        'Lt Optic Nerve': [0, 0, 128], # Navy        'Brain Stem': [128, 128, 0],# Olive        'Lt Lung': [128, 0, 128],   # Purple        'Rt Lung': [0, 128, 128]    # Teal    }    for patient_folder in os.listdir(nifti_root_folder):        patient_path = os.path.join(nifti_root_folder, patient_folder)        if not os.path.isdir(patient_path):            continue        print(f"Processing patient: {patient_folder}")        for root, dirs, files in os.walk(patient_path):            ct_file = next((f for f in files if f == 'ct_volume.nii.gz'), None)            if ct_file:                print(f"Processing folder: {root}")                ct_path = os.path.join(root, ct_file)                ct_nifti = nib.load(ct_path)                ct_data = ct_nifti.get_fdata()                # Normalize CT data to 0-255 range                ct_data = ((ct_data - ct_data.min()) / (ct_data.max() - ct_data.min()) * 255).astype(np.uint8)                # Create output folders                rel_path = os.path.relpath(root, nifti_root_folder)                ct_output_path = os.path.join(output_root_folder, rel_path, 'ct_slices')                mask_output_path = os.path.join(output_root_folder, rel_path, 'mask_slices')                os.makedirs(ct_output_path, exist_ok=True)                os.makedirs(mask_output_path, exist_ok=True)                # Load mask data                masks = {}                for structure in structures_of_interest:                    mask_file = f'{structure.lower().replace(" ", "_")}_mask.nii.gz'                    mask_path = os.path.join(root, mask_file)                    if os.path.exists(mask_path):                        mask_nifti = nib.load(mask_path)                        masks[structure] = mask_nifti.get_fdata()                # Process each slice                valid_slices = []                for i in range(ct_data.shape[2]):                    has_structure = False                    for structure, mask in masks.items():                        if np.any(mask[:,:,i]):                            has_structure = True                            break                    if has_structure:                        valid_slices.append(i)                        # Save CT slice                        ct_slice = ct_data[:, :, i]                        ct_img = Image.fromarray(ct_slice)                        ct_img.save(os.path.join(ct_output_path, f'ct_slice_{i:03d}.png'))                        # Save individual binary masks                        combined_mask = np.zeros((*ct_data.shape[:2], 3), dtype=np.uint8)                        for structure, mask in masks.items():                            structure_slice = mask[:, :, i]                            binary_mask = Image.fromarray((structure_slice * 255).astype(np.uint8))                            binary_mask.save(os.path.join(mask_output_path, f'{structure.lower().replace(" ", "_")}_{i:03d}.png'))                                                        # Add to combined color mask for visualization                            color = color_map[structure]                            for c in range(3):                                combined_mask[:, :, c] += (structure_slice * color[c]).astype(np.uint8)                        # Save combined color mask                        combined_mask_img = Image.fromarray(combined_mask)                        combined_mask_img.save(os.path.join(mask_output_path, f'combined_mask_{i:03d}.png'))                print(f"Saved CT slices and masks to {ct_output_path} and {mask_output_path}")                # Create random samples with embedded masks                sample_output_path = os.path.join(output_root_folder, rel_path, 'samples')                os.makedirs(sample_output_path, exist_ok=True)                num_samples = min(5, len(valid_slices))  # Choose up to 5 random samples                for sample in random.sample(valid_slices, num_samples):                    ct_slice = ct_data[:, :, sample]                    combined_mask = np.zeros((*ct_data.shape[:2], 3), dtype=np.uint8)                    for structure, mask in masks.items():                        structure_slice = mask[:, :, sample]                        color = color_map[structure]                        for c in range(3):                            combined_mask[:, :, c] += (structure_slice * color[c]).astype(np.uint8)                                        # Embed mask in CT slice                    ct_rgb = np.stack([ct_slice, ct_slice, ct_slice], axis=2)                    embedded = np.where(combined_mask > 0, combined_mask, ct_rgb)                    embedded_img = Image.fromarray(embedded)                    embedded_img.save(os.path.join(sample_output_path, f'sample_embedded_{sample:03d}.png'))                print(f"Saved sample embedded images to {sample_output_path}")# Usagenifti_root_folder = '/Users/zubairsaeed/Downloads/PhD/H&N/Patients/H&N-Organized/NIfTI'output_root_folder = '/Users/zubairsaeed/Downloads/PhD/H&N/Patients/H&N-Organized/PNG'structures_of_interest = [    'GTV1', 'Spinal Cord', 'Rt Parotid', 'Lt Parotid', 'Mandible',    'Rt Eye', 'Lt Eye', 'Rt Optic Nerve', 'Lt Optic Nerve',    'Brain Stem', 'Lt Lung', 'Rt Lung']nifti_to_png_slices_and_masks(nifti_root_folder, output_root_folder, structures_of_interest)