def get_object_type_qconfig(
        qconfig_dict: Any,
        object_type: Union[Callable, str],
        fallback_qconfig: QConfigAny) -> QConfigAny:
    # object_type can be
    # 1. module type (call_module)
    # 2. function (call_function)
    # 3. string (call_method)
    return qconfig_dict['object_type'].get(
        object_type, fallback_qconfig)
