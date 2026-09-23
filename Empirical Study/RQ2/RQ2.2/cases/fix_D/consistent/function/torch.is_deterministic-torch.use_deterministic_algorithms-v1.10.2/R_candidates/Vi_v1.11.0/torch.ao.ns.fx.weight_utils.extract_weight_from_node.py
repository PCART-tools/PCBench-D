def extract_weight_from_node(
    node: Node,
    gm: GraphModule,
    op_to_type_to_weight_extraction_fn: Optional[Dict[str, Dict[Callable, Callable]]] = None,
) -> Optional[NSSingleResultType]:
    res_type = NSSingleResultValuesType.WEIGHT.value

    # Not all graphmodules have _node_name_to_scope, so only fill it
    # out if it exists.
    fqn = None
    if hasattr(gm, '_node_name_to_scope'):
        fqn = gm._node_name_to_scope[node.name][0]  # type: ignore[index]

    if op_to_type_to_weight_extraction_fn is None:
        op_to_type_to_weight_extraction_fn = get_op_to_type_to_weight_extraction_fn()

    ref_node_type = get_target_type_str(node, gm)
    # for extracting weights, these are always the same
    prev_node_type = ref_node_type

    if node.op == 'call_function':
        function_mapping = op_to_type_to_weight_extraction_fn['call_function']
        for target_fn_type, weight_extraction_fn in function_mapping.items():
            if node.target == target_fn_type:
                weight = weight_extraction_fn(node, gm)
                return {
                    'type': res_type,
                    'values': [weight],
                    'prev_node_name': node.name,
                    'prev_node_target_type': prev_node_type,
                    'ref_node_name': node.name,
                    'ref_node_target_type': ref_node_type,
                    'index_within_arg': 0,
                    'index_of_arg': 0,
                    'fqn': fqn,
                }

    elif node.op == 'call_module':
        # for call_module, we need to look up the modules to do the type check
        assert isinstance(node.target, str)
        mod = getattr_from_fqn(gm, node.target)
        module_mapping = op_to_type_to_weight_extraction_fn['call_module']
        for target_mod_type, weight_extraction_fn in module_mapping.items():
            if type(mod) == target_mod_type:
                weight = weight_extraction_fn(mod)
                return {
                    'type': res_type,
                    'values': [weight],
                    'prev_node_name': node.name,
                    'prev_node_target_type': prev_node_type,
                    'ref_node_name': node.name,
                    'ref_node_target_type': ref_node_type,
                    'index_within_arg': 0,
                    'index_of_arg': 0,
                    'fqn': fqn,
                }

    return None
