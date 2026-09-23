def check_is_valid_qconfig_dict(qconfig_dict: Any) -> None:
    r""" Checks if the given qconfig_dict has the correct keys

    Args:
      `qconfig_dict`: dictionary whose keys we want to check
    """

    qconfig_dict_allowed_keys = {
        "", "object_type", "module_name_regex", "module_name",
        "module_name_object_type_order"}
    check_is_valid_config_dict(qconfig_dict, qconfig_dict_allowed_keys, "qconfig_dict")
