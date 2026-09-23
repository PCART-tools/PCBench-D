def check_is_valid_prepare_custom_config_dict(prepare_custom_config_dict: Dict[str, Any] = None) -> None:
    r""" Checks if the given prepare_custom_config_dict has the correct keys

    Args:
      `prepare_custom_config_dict`: customization configuration dictionary for
      quantization tool
    """
    if not prepare_custom_config_dict:
        return

    prepare_custom_config_dict_allowed_keys = {"standalone_module_name",
                                               "standalone_module_class",
                                               "float_to_observed_custom_module_class",
                                               "non_traceable_module_name",
                                               "non_traceable_module_class",
                                               "additional_fuser_method_mapping",
                                               "additional_qat__module_mapping",
                                               "additional_fusion_pattern",
                                               "additional_quant_pattern",
                                               "input_quantized_idxs",
                                               "output_quantized_idxs",
                                               "preserved_attributes"}
    check_is_valid_config_dict(prepare_custom_config_dict,
                               prepare_custom_config_dict_allowed_keys, "prepare_custom_config_dict")
