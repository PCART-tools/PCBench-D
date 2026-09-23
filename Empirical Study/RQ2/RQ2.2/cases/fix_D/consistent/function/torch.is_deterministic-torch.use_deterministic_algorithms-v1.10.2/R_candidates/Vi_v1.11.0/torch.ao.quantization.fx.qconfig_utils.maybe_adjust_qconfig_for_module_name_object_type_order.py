def maybe_adjust_qconfig_for_module_name_object_type_order(
    qconfig_dict: Any,
    cur_module_path: str,
    cur_object_type: Callable,
    cur_object_type_idx: int,
    fallback_qconfig: QConfigAny,
) -> QConfigAny:
    qconfig_module_name_object_type_order = \
        qconfig_dict.get('module_name_object_type_order', {})
    for module_path, object_type, object_type_idx, qconfig in \
            qconfig_module_name_object_type_order:
        if (
            (module_path == cur_module_path) and
            (object_type == cur_object_type) and
            (object_type_idx == cur_object_type_idx)
        ):
            return qconfig

    return fallback_qconfig
