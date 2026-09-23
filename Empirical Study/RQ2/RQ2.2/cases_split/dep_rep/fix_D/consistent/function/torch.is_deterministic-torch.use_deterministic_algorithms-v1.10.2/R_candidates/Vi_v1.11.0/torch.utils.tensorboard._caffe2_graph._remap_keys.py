def _remap_keys(old_dict, rename_fn):
    '''
    Rename keys of 'old_dict' according to 'rename_fn'.

    Args:
        old_dict: Dictionary (i.e. containing blob_name -> blob_name
            relationships.)
        remap_fn: Function string -> string for renaming.

    Returns:
        None. Modifies old_dict in-place.
    '''
    new_dict = {rename_fn(key): value for key,
                value in old_dict.items()}
    old_dict.clear()
    old_dict.update(new_dict)
