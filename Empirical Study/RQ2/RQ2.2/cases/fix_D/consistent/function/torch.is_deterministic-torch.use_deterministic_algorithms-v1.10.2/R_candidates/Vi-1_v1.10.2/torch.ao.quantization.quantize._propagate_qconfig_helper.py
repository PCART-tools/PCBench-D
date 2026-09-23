def _propagate_qconfig_helper(module, qconfig_dict, allow_list=None,
                              qconfig_parent=None, prefix=''):
    r"""This is a helper function for `propagate_qconfig_`

    Args:
        module: input module
        qconfig_dict: dictionary that maps from name of submodule to quantization
                     configuration
        allow_list: list of quantizable modules
        qconfig_parent: quantization config of parent module, we will fallback to
                       this config when there is no specified config for current
                       module
        prefix: corresponding prefix of the current module, used as key in
                qconfig_dict

    Return:
        None, module is modified inplace with qconfig attached
    """
    # TODO: Add test
    if allow_list is None:
        allow_list = get_default_qconfig_propagation_list()

    module_qconfig = qconfig_dict.get(type(module), qconfig_parent)
    module_qconfig = qconfig_dict.get(prefix, module_qconfig)
    module_qconfig = getattr(module, 'qconfig', module_qconfig)

    torch.quantization.qconfig.assert_valid_qconfig(module_qconfig, module)

    qconfig_with_device_check = add_module_to_qconfig_obs_ctr(module_qconfig, module)
    module.qconfig = qconfig_with_device_check

    for name, child in module.named_children():
        module_prefix = prefix + '.' + name if prefix else name
        _propagate_qconfig_helper(child, qconfig_dict, allow_list,
                                  qconfig_with_device_check, module_prefix)
