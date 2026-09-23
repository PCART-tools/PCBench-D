def swap_custom_module_to_observed(
        node: Node,
        qconfig: QConfigAny,
        modules: Dict[str, torch.nn.Module],
        prepare_custom_config_dict: Dict[str, Any]):
    custom_module = modules[node.target]  # type: ignore[index]
    custom_module_class_mapping = prepare_custom_config_dict.get(
        "float_to_observed_custom_module_class", {})
    observed_custom_module_class = \
        get_swapped_custom_module_class(
            custom_module, custom_module_class_mapping, qconfig)
    observed_custom_module = \
        observed_custom_module_class.from_float(custom_module)
    parent_name, name = _parent_name(node.target)
    setattr(modules[parent_name], name, observed_custom_module)
