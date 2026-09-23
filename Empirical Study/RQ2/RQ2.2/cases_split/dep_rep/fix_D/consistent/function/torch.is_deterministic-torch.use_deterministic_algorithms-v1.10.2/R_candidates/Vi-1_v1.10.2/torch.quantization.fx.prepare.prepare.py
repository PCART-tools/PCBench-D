def prepare(
        model: GraphModule,
        qconfig_dict: Any,
        node_name_to_scope: Dict[str, Tuple[str, type]],
        prepare_custom_config_dict: Optional[Dict[str, Any]] = None,
        equalization_qconfig_dict: Optional[Dict[str, Any]] = None,
        backend_config_dict: Optional[Dict[str, Any]] = None,
        is_standalone_module: bool = False) -> ObservedGraphModule:
    """ standalone_module means it a submodule that is not inlined in
    parent module, and will be quantized separately as one unit.

    How the standalone module is observed is specified by `input_quantized_idxs` and
    `output_quantized_idxs` in the prepare_custom_config for the standalone module
    Args:
        node_name_to_scope: mapping from node name to the scope of the module which contains the node.
        The scope is a tuple of fully qualified path of the module and the type of the module
    Returns:
        model(GraphModule): prepared standalone module
        attributes:
            _standalone_module_input_quantized_idxs(List[Int]): a list of
                indexes for the graph input that is expected to be quantized,
                same as input_quantized_idxs configuration provided
                for the standalone module
            _standalone_module_output_quantized_idxs(List[Int]): a list of
                indexs for the graph output that is quantized
                same as input_quantized_idxs configuration provided
                for the standalone module
    """
    if prepare_custom_config_dict is None:
        prepare_custom_config_dict = {}
    if equalization_qconfig_dict is None:
        equalization_qconfig_dict = {}
    if backend_config_dict is None:
        backend_config_dict = get_fbgemm_backend_config_dict()

    validate_backend_config_dict(backend_config_dict)

    additional_quant_patterns = \
        prepare_custom_config_dict.get("additional_quant_pattern", {})
    # mapping from a tuple of nodes in reverse order to uninitialized
    #   QuantizeHandler subclass. For example,
    # {
    #   # match a single node
    #   (<class 'torch.nn.modules.conv.Conv3d'>:
    #     <class 'torch.quantization.fx.quantize.ConvRelu'>),
    #   # match multiple nodes in reverse order
    #   ((<function relu at 0x7f766a7360d0>, <built-in function add>):
    #     <class 'torch.quantization.fx.quantize.Add'>),
    # }
    quant_patterns = backend_config_dict["quant_patterns"]
    patterns: Dict[Pattern, QuantizeHandler] = get_combined_dict(
        quant_patterns, additional_quant_patterns)

    convert_dict_to_ordered_dict(qconfig_dict)
    convert_dict_to_ordered_dict(equalization_qconfig_dict)
    flattened_qconfig_dict = get_flattened_qconfig_dict(qconfig_dict)
    # TODO: support regex as well
    propagate_qconfig_(model, flattened_qconfig_dict)

    if model.training:
        additional_qat_module_mapping = prepare_custom_config_dict.get(
            "additional_qat_module_mapping", {})
        qat_swap_modules(model, additional_qat_module_mapping)
        qconfig_dict = update_qconfig_for_qat(qconfig_dict, additional_qat_module_mapping)

    qconfig_dict = update_qconfig_for_fusion(model, qconfig_dict)
    equalization_qconfig_dict = update_qconfig_for_fusion(model, equalization_qconfig_dict)

    # mapping from fully qualified module name to module instance
    # for example,
    # {
    #   '': Model(...),
    #   'linear': Linear(...),
    #   'linear.weight_fake_quant': PerChannelMinMaxObserver(...),
    # }
    modules = dict(model.named_modules())

    # fill qconfig_map, a map from node name to qconfig, used in find_matches
    equalization_qconfig_map = generate_qconfig_map(model, modules, model.graph, equalization_qconfig_dict, node_name_to_scope)
    qconfig_map = generate_qconfig_map(model, modules, model.graph, qconfig_dict, node_name_to_scope)

    # match the patterns that will get quantized
    standalone_module_name_configs = prepare_custom_config_dict.get(
        "standalone_module_name", [])
    standalone_module_class_configs = prepare_custom_config_dict.get(
        "standalone_module_class", [])

    standalone_module_names = [config[0] for config in standalone_module_name_configs]
    standalone_module_classes = [config[0] for config in standalone_module_class_configs]
    custom_module_classes = get_custom_module_class_keys(
        prepare_custom_config_dict, "float_to_observed_custom_module_class")
    matches = find_matches(
        model.graph, modules, patterns, qconfig_map, standalone_module_names,
        standalone_module_classes, custom_module_classes)

    input_quantized_idxs: List[int] = prepare_custom_config_dict.get(
        "input_quantized_idxs", [])
    output_quantized_idxs: List[int] = prepare_custom_config_dict.get(
        "output_quantized_idxs", [])

    run_prepare_fx_on_standalone_modules(
        model, modules, matches, prepare_custom_config_dict)

    result_node = insert_observers_for_model(
        model, modules, matches, qconfig_map,
        model.graph, prepare_custom_config_dict,
        equalization_qconfig_map,
        input_quantized_idxs, output_quantized_idxs)

    save_state(model, qconfig_map, node_name_to_scope, patterns,
               prepare_custom_config_dict, equalization_qconfig_map)
    preserved_attributes = set(prepare_custom_config_dict.get("preserved_attributes", []))
    model = ObservedGraphModule(model, model.graph, preserved_attributes)
    if is_standalone_module:
        assert result_node is not None
        assert isinstance(result_node.args[0], Node), \
            "standalone module only supports returning simple value currently"\
            "(not tuple, dict etc.)"
        # these inputs are observed in parent
        # converting List[int] to Tensor since module attribute is
        # Union[Tensor, Module]
        model._standalone_module_input_quantized_idxs = \
            torch.tensor(input_quantized_idxs)
        model._standalone_module_output_quantized_idxs = torch.tensor(output_quantized_idxs)
    return model
