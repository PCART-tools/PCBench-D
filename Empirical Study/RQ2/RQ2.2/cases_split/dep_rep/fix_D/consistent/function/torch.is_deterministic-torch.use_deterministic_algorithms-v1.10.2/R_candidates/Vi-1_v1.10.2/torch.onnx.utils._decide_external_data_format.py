def _decide_external_data_format(use_external_data_format, operator_export_type, f):
    val_use_external_data_format = _resolve_args_by_export_type("use_external_data_format",
                                                                use_external_data_format,
                                                                operator_export_type)
    # f can be a non-string in regular-sized model export case, but for large model export, f must be a non-empty
    # string specifying the location of the model. For large model cases, if f is not a non-empty string,
    # then this method returns an empty string, which is an error condition for the large model export code
    # path later (but not for regular model export code path).
    if (val_use_external_data_format is None or val_use_external_data_format is True) and isinstance(f, str):
        model_file_location = f
    else:
        model_file_location = str()
    return val_use_external_data_format, model_file_location
