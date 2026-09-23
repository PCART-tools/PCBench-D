def compare_prepare_convert_qconfig_dict(prepare_qconfig_dict: Dict[str, Dict[Any, Any]],
                                         convert_qconfig_dict: Dict[str, Dict[Any, Any]]) -> None:
    r""" Compare the qconfig_dict passed in convert to the one from prepare and check the values

    Args:
      `prepare_qconfig_dict`: configuration dictionary for prepare quantization step
      `convert_qconfig_dict`: configuration dictionary for convert quantization step
    """
    prepare_keys = prepare_qconfig_dict.keys()
    convert_keys = convert_qconfig_dict.keys()

    for k in prepare_keys:
        if k == '':
            assert k in convert_qconfig_dict, "Missing key {} from convert qconfig_dict when it was present in prepare".format(k)
            assert (convert_qconfig_dict[k] is None
                   or qconfig_equals(prepare_qconfig_dict[k], convert_qconfig_dict[k])), (  # type: ignore[arg-type]
                "Expected convert qconfig_dict have the same qconfig as prepare qconfig_dict or None."
                "Updated qconfig {} to {} for key {}".format(prepare_qconfig_dict[k], convert_qconfig_dict[k], k))
        elif k in ['object_type', 'module_name', 'module_namr_regex']:
            for name, qconfig in prepare_qconfig_dict[k].items():
                assert name in convert_qconfig_dict[k], "Missing key {} {} from convert qconfig_dict \
                when it was present in prepare".format(k, name)
                assert convert_qconfig_dict[k][name] is None \
                    or qconfig_equals(prepare_qconfig_dict[k][name], convert_qconfig_dict[k][name]), \
                    "Expected convert qconfig_dict have the same qconfig as prepare qconfig_dict or None. \
                    Updated qconfig {} to {} for key {} {}".format(prepare_qconfig_dict[k], convert_qconfig_dict[k], k, name)
        else:
            assert "Unsupported key in convert_qconfig_dict {}".format(k)
