def check_is_valid_convert_custom_config_dict(convert_custom_config_dict: Optional[Dict[str, Any]] = None) -> None:
    r""" Checks if the given convert_custom_config_dict has the correct keys

    Args:
      `convert_custom_config_dict`: dictionary for custom configurations for
      convert function
    """
    if not convert_custom_config_dict:
        return

    convert_custom_config_dict_allowed_keys = {"additional_object_mapping",
                                               "observed_to_quantized_custom_module_class",
                                               "preserved_attributes"}
    check_is_valid_config_dict(convert_custom_config_dict,
                               convert_custom_config_dict_allowed_keys, "convert_custom_config_dict")
