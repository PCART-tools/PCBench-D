def _resolve_args_by_export_type(arg_name, arg_value, operator_export_type):
    # This helper method resolves the arguments that are ignored when export_type != operator_export_type.ONNX
    if operator_export_type is not operator_export_type.ONNX:
        if arg_value is True:
            warnings.warn("`{}' can be set to True only when 'operator_export_type' is "
                          "`ONNX`. Since 'operator_export_type' is not set to 'ONNX', "
                          "`{}` argument will be ignored.".format(arg_name, arg_name))
        arg_value = False
    return arg_value
