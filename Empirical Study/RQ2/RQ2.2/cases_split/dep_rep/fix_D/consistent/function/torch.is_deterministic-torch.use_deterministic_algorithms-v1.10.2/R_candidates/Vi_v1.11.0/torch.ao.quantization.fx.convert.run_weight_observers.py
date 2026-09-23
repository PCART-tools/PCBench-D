def run_weight_observers(observed: GraphModule) -> None:
    r''' Extract the subgraph that produces the weight for dynamic quant
    or weight only quant node and run the subgraph to observe the weight.
    Note that the observers of dynamic quant or weight only quant ops are
    run during the convert step.
    '''
    for node in observed.graph.nodes:
        if node.op == 'call_function' and node.target in WEIGHT_INDEX_DICT:
            for i, node_arg in enumerate(node.args):
                if i in WEIGHT_INDEX_DICT[node.target]:
                    # node_arg is weight
                    weight_observer_nodes = collect_producer_nodes(node_arg)
                    if weight_observer_nodes is not None:
                        weight_observer_module = \
                            graph_module_from_producer_nodes(
                                observed, weight_observer_nodes)
                        # run the weight observer
                        weight_observer_module()
