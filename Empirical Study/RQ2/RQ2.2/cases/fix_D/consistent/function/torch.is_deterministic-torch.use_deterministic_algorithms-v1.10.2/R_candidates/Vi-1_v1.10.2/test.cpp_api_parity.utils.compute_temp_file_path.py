def compute_temp_file_path(cpp_tmp_folder, variant_name, file_suffix):
    return os.path.join(cpp_tmp_folder, '{}_{}.pt'.format(variant_name, file_suffix))
