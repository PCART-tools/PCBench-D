def get_module_name_qconfig(qconfig_dict, module_name, fallback_qconfig):
    if module_name == '':
        # module name qconfig not found
        return fallback_qconfig
    if module_name in qconfig_dict['module_name']:
        return qconfig_dict['module_name'][module_name]
    else:
        parent, _ = _parent_name(module_name)
        return get_module_name_qconfig(qconfig_dict, parent, fallback_qconfig)
