def extract_weights(
    model_name_a: str,
    model_a: nn.Module,
    model_name_b: str,
    model_b: nn.Module,
    base_name_to_sets_of_related_ops: Optional[Dict[str, Set[NSNodeTargetType]]] = None,
    unmatchable_types_map: Optional[Dict[str, Set[NSNodeTargetType]]] = None,
    op_to_type_to_weight_extraction_fn: Optional[Dict[str, Dict[Callable, Callable]]] = None,
) -> NSResultsType:
    torch._C._log_api_usage_once("quantization_api._numeric_suite_fx.extract_weights")
    if base_name_to_sets_of_related_ops is None:
        base_name_to_sets_of_related_ops = \
            get_base_name_to_sets_of_related_ops()
    type_a_related_to_b = \
        get_type_a_related_to_b(base_name_to_sets_of_related_ops)

    # TODO(future PR): expose these
    skipped_module_names: List[str] = []
    skipped_module_classes: List[Callable] = []
    tracer_a = NSTracer(skipped_module_names, skipped_module_classes)
    tracer_b = NSTracer(skipped_module_names, skipped_module_classes)
    gm_a = GraphModule(model_a, tracer_a.trace(model_a))
    if hasattr(model_a, '_node_name_to_scope'):
        gm_a._node_name_to_scope = model_a._node_name_to_scope
    gm_b = GraphModule(model_b, tracer_b.trace(model_b))
    if hasattr(model_b, '_node_name_to_scope'):
        gm_b._node_name_to_scope = model_b._node_name_to_scope
    return _extract_weights_impl(
        model_name_a, gm_a, model_name_b, gm_b, base_name_to_sets_of_related_ops,
        unmatchable_types_map, op_to_type_to_weight_extraction_fn)
