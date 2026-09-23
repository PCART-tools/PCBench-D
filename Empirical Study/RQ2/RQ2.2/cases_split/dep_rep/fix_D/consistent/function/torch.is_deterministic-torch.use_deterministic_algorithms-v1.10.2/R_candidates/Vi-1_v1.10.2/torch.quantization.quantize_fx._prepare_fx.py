def _prepare_fx(model: torch.nn.Module,
                qconfig_dict: Any,
                prepare_custom_config_dict: Optional[Dict[str, Any]] = None,
                equalization_qconfig_dict: Optional[Dict[str, Any]] = None,
                backend_config_dict: Optional[Dict[str, Any]] = None,
                is_standalone_module: bool = False) -> ObservedGraphModule:
    r""" Internal helper function for prepare_fx
    Args:
      `model`, `qconfig_dict`, `prepare_custom_config_dict`, `equalization_qonfig_dict`:
      see docs for :func:`~torch.quantization.prepare_fx`
      `is_standalone_module`: a boolean flag indicates whether we are
      quantizing a standalone module or not, a standalone module
      is a submodule of the parent module that is not inlined in the
forward graph of the parent module,
      the way we quantize standalone module is described in:
      :func:`~torch.quantization._prepare_standalone_module_fx`
    """
    if prepare_custom_config_dict is None:
        prepare_custom_config_dict = {}
    if equalization_qconfig_dict is None:
        equalization_qconfig_dict = {}

    check_is_valid_qconfig_dict(qconfig_dict)
    check_is_valid_prepare_custom_config_dict(prepare_custom_config_dict)
    check_is_valid_qconfig_dict(equalization_qconfig_dict)

    skipped_module_names = prepare_custom_config_dict.get("non_traceable_module_name", [])
    skipped_module_classes = prepare_custom_config_dict.get("non_traceable_module_class", [])

    # swap FloatFunctional with FXFloatFunctional
    _swap_ff_with_fxff(model)

    # symbolically trace the model
    if not is_standalone_module:
        # standalone module and custom module config are applied in top level module
        standalone_module_name_configs = prepare_custom_config_dict.get("standalone_module_name", [])
        skipped_module_names += [config[0] for config in standalone_module_name_configs]

        standalone_module_class_configs = prepare_custom_config_dict.get("standalone_module_class", [])
        skipped_module_classes += [config[0] for config in standalone_module_class_configs]
        float_custom_module_classes = get_custom_module_class_keys(
            prepare_custom_config_dict, "float_to_observed_custom_module_class")
        skipped_module_classes += float_custom_module_classes

    preserved_attributes = prepare_custom_config_dict.get("preserved_attributes", [])
    tracer = QuantizationTracer(
        skipped_module_names, skipped_module_classes)
    graph_module = GraphModule(model, tracer.trace(model))
    for attr_name in preserved_attributes:
        setattr(graph_module, attr_name, getattr(model, attr_name))
    graph_module = _fuse_fx(graph_module, prepare_custom_config_dict)
    prepared = prepare(
        graph_module,
        qconfig_dict,
        tracer.node_name_to_scope,
        prepare_custom_config_dict=prepare_custom_config_dict,
        equalization_qconfig_dict=equalization_qconfig_dict,
        backend_config_dict=backend_config_dict,
        is_standalone_module=is_standalone_module)

    for attr_name in preserved_attributes:
        setattr(prepared, attr_name, getattr(model, attr_name))
    return prepared
