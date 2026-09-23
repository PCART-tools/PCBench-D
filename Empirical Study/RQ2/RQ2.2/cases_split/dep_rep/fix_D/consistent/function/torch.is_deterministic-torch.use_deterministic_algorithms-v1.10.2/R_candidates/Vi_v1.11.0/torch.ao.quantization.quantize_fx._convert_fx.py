def _convert_fx(
    graph_module: GraphModule,
    is_reference: bool,
    convert_custom_config_dict: Optional[Dict[str, Any]] = None,
    is_standalone_module: bool = False,
    _remove_qconfig: bool = True,
    qconfig_dict: Dict[str, Any] = None,
) -> torch.nn.Module:
    """ `is_standalone_module`: see docs in :func:`~torch.ao.quantization.prepare_standalone_module_fx`
    """
    if convert_custom_config_dict is None:
        convert_custom_config_dict = {}

    _check_is_graph_module(graph_module)
    check_is_valid_convert_custom_config_dict(convert_custom_config_dict)

    quantized = convert(
        graph_module,
        is_reference,
        convert_custom_config_dict,
        is_standalone_module,
        _remove_qconfig_flag=_remove_qconfig,
        convert_qconfig_dict=qconfig_dict,
    )

    preserved_attributes = convert_custom_config_dict.get("preserved_attributes", [])
    for attr_name in preserved_attributes:
        setattr(quantized, attr_name, getattr(graph_module, attr_name))
    return quantized
