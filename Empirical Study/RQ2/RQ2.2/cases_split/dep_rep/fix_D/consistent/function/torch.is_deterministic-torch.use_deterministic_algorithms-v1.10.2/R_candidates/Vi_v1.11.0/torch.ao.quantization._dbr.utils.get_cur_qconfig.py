def get_cur_qconfig(
    qconfig_dict: Dict[str, Any],
    cur_fqn: str,
    cur_op_type: Callable,
) -> Optional[QConfigAny]:
    # precedence: global -> object_type -> module_name_regex -> module_name
    #   -> module_name_object_type_order
    # (module_name_regex, module_name_object_type_order not implemented yet)

    # global
    global_qconfig = qconfig_dict['']

    qconfig = maybe_adjust_qconfig_for_module_type_or_name(
        qconfig_dict, cur_op_type, cur_fqn, global_qconfig)

    return qconfig
