def fold_weight(
        quantized: QuantizedGraphModule,
        node_name_to_scope: Dict[str, Tuple[str, type]]) -> QuantizedGraphModule:
    """
    Trace back from the weight node util we hit getattr, reconstruct the
    graph module with the traced nodes and run the graph module to pack the
    weight. then replace the original chain of ops with the packed weight.
    """
    packed_weights = dict()
    # map from folded node name to the prepacked weight name
    folded_nodes = dict()
    # get packed weights
    for node in quantized.graph.nodes:
        if node.op == 'call_function' and node.target in WEIGHT_PREPACK_OPS:
            nodes_to_fold = collect_producer_nodes(node)
            if nodes_to_fold is not None:
                for node_to_fold in nodes_to_fold:
                    folded_nodes[node_to_fold.name] = node

                prepacking_module = graph_module_from_producer_nodes(
                    quantized, nodes_to_fold)
                packed_weight = prepacking_module()
                packed_weights[node.name] = packed_weight

    # remove folded nodes and replace the prepacking node with getattr
    folded_graph = Graph()
    env: Dict[Any, Any] = {}

    def load_arg(a):
        return map_arg(a, lambda node: env[node.name])
    quantized_root = quantized
    quantized_graph = quantized.graph

    for node in quantized_graph.nodes:
        prepack_node = folded_nodes.get(node.name, None)
        if prepack_node is node:
            packed_weight = packed_weights[node.name]
            # add a prepacked attribute to root
            op_node = list(prepack_node.users)[0]
            module_path, _ = node_name_to_scope[op_node.name]
            get_new_packed_weight_name = \
                get_new_attr_name_with_prefix(module_path + '_packed_weight_')
            packed_weight_name = get_new_packed_weight_name(quantized_root)
            setattr(quantized_root, packed_weight_name, packed_weight)
            # replace prepack node with a getattr node
            env[node.name] = folded_graph.create_node(
                'get_attr', packed_weight_name, (), {})
        elif prepack_node is not None:
            # remove the foled node
            continue
        else:
            # copy other nodes
            env[node.name] = folded_graph.node_copy(node, load_arg)
    quantized = QuantizedGraphModule(quantized_root, folded_graph, quantized_root.preserved_attr_names)
    return quantized
