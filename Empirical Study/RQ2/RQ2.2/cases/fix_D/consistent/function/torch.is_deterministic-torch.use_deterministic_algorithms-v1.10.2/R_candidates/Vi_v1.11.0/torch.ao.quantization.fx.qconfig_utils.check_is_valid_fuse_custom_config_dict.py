def check_is_valid_fuse_custom_config_dict(fuse_custom_config_dict: Optional[Dict[str, Any]] = None) -> None:
    r""" Checks if the given fuse_custom_config_dict has the correct keys

    Args:
      `fuse_custom_config_dict`: dictionary for custom configurations for fuse_fx
    """
    if not fuse_custom_config_dict:
        return

    fuse_custom_config_dict_allowed_keys = {"additional_fuser_method_mapping",
                                            "preserved_attributes"}
    check_is_valid_config_dict(fuse_custom_config_dict, fuse_custom_config_dict_allowed_keys, "fuse_custom_config_dict")
