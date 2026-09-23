def save_model_states(
    state_dict,
    sparsified_model_dump_path,
    save_file_name,
    sparse_block_shape,
    norm,
    zip=True,
):
    """Dumps the state_dict() of the model.

    Args:
        state_dict (Dict)
            The state_dict() as dumped by dlrm_s_pytorch.py. Only the model state will be extracted
            from this dictionary. This corresponds to the 'state_dict' key in the state_dict dictionary.
            >>> model_state = state_dict['state_dict']
        save_file_name (str)
            The filename (not path) when saving the model state dictionary
        sparse_block_shape (Tuple)
            The block shape corresponding to the data norm sparsifier. **Used for creating save directory**
        norm (str)
            type of norm (L1, L2) for the datanorm sparsifier. **Used for creating save directory**
        zip (bool)
            if True, the file is zip-compressed.
    """
    folder_name = os.path.join(sparsified_model_dump_path, str(norm))

    # save model only states
    folder_str = f"config_{sparse_block_shape}"
    model_state = state_dict["state_dict"]
    model_state_path = os.path.join(folder_name, folder_str, save_file_name)

    os.makedirs(os.path.dirname(model_state_path), exist_ok=True)
    torch.save(model_state, model_state_path)

    if zip:
        zip_path = model_state_path.replace(".ckpt", ".zip")
        with ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip:
            zip.write(model_state_path, save_file_name)
        os.remove(model_state_path)  # store it as zip, remove uncompressed
        model_state_path = zip_path

    model_state_path = os.path.abspath(model_state_path)
    file_size = os.path.getsize(model_state_path)
    file_size = file_size >> 20  # size in mb
    return model_state_path, file_size
