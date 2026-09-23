def _convert(
        module, mapping=None, inplace=False,
        convert_custom_config_dict=None):
    r"""Converts submodules in input module to a different module according to `mapping`
    by calling `from_float` method on the target module class

    Args:
        module: input module
        mapping: a dictionary that maps from source module type to target
                 module type, can be overwritten to allow swapping user defined
                 Modules
        inplace: carry out model transformations in-place, the original module
                 is mutated

    """
    if mapping is None:
        mapping = get_default_static_quant_module_mappings()
    if convert_custom_config_dict is None:
        convert_custom_config_dict = {}
    custom_module_class_mapping = convert_custom_config_dict.get("observed_to_quantized_custom_module_class", {})

    if not inplace:
        module = copy.deepcopy(module)
    reassign = {}
    for name, mod in module.named_children():
        # both fused modules and observed custom modules are
        # swapped as one unit
        if not isinstance(mod, _FusedModule) and \
           type(mod) not in custom_module_class_mapping:
            _convert(mod, mapping, True,  # inplace
                     convert_custom_config_dict)
        reassign[name] = swap_module(mod, mapping, custom_module_class_mapping)

    for key, value in reassign.items():
        module._modules[key] = value

    return module
