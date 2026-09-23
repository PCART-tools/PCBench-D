def quantize_node(
        in_node: Node,
        obs_module: torch.nn.Module,
        obs_node: Node,
        modules: Dict[str, torch.nn.Module],
        quantized_graph: Graph,
        node_name_to_scope: Dict[str, Tuple[str, type]],
        is_input: bool) -> Node:
    ''' Add quantization nodes (eg. quantize_per_tensor/per_channel) for given node to graph
    with the qparams calculated from activation_post_process (obs_module).
    The observer node (obs_node) is used to find the FQN of the user of act_post_process.
    e.g. Given input `node` in `node = self.conv(x)`, insert node:
    `quantized_node = torch.quantize_per_tensor(x, self._scale_0, self._zer_point_0, self._dtype_0)`
    where self._scale_0, self._zero_point_0 and self._dtype_0 are
    calculated from `obs_module`
    '''
    # Find the first use of the observer node, we use this to get the scope of the module.
    if is_input:
        # if the quantize function is at the input of op, then we find the first user of the observer_node
        # to get the path. If a linear call_function is in the user list, we return the first instance
        # of linear node to get the FQN.
        users = list(obs_node.users)
        first_linear_use_or_first_use = users[0] if users else None
        linear_node = None
        for n in users:
            if n.op == "call_function" and n.target == torch.nn.functional.linear:
                linear_node = n
                break
        if linear_node:
            first_linear_use_or_first_use = linear_node
        prefix = "_input"
    else:
        # if the quantize function is at the output of the op, we use the observer input node to get the path
        first_linear_use_or_first_use = in_node
        prefix = "_output"

    if first_linear_use_or_first_use and first_linear_use_or_first_use.name in node_name_to_scope:
        module_path, _ = node_name_to_scope[first_linear_use_or_first_use.name]
    else:
        # TODO: it's not used, so actually we can skip quantization
        # but this requires changing return type of quantize_node
        # we can fix it later if needed
        module_path = ""
    root_module = modules['']
    graph = quantized_graph
    node_type, quantize_op, qparams = get_quantize_node_info(obs_module)
    inputs = [in_node]

    for key, value in qparams.items():
        if key in ['_scale_', '_zero_point_']:
            # For scale and zero_point values we register them as buffers in the root module.
            qparam_node = create_getattr_from_value(root_module, graph, module_path + prefix + key, value)
            inputs.append(qparam_node)
        else:
            # for qparams that are not scale/zero_point (like axis, dtype) we store them as literals in the graph.
            inputs.append(value)
    return graph.create_node(node_type, quantize_op, tuple(inputs), {})
