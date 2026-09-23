def build_edge(layer, graph, reformat_layers, output_name2node, layer_name2node):
    if layer.input_names is None:
        return

    for input_name, input_type in zip(layer.input_names, layer.input_types):
        if input_name not in output_name2node:
            if input_name in reformat_layers:
                from_node = pydot.Node(
                    input_name,
                    label="{reformatter|kernel: Reformat\\l|tactic: 0\\l}",
                    **style,
                )
                graph.add_node(from_node)
                if reformat_layers[input_name][0] in output_name2node:
                    graph.add_edge(
                        pydot.Edge(
                            output_name2node[reformat_layers[input_name][0]],
                            from_node,
                            label=f"{reformat_layers[input_name][0]}\\l{reformat_layers[input_name][1]}\\l",
                        )
                    )
            else:
                print(f"Missing node {input_name}")
                from_node = input_name
        else:
            from_node = output_name2node[input_name]

        edge_name = input_name.replace(">", "\\>")
        graph.add_edge(
            pydot.Edge(
                from_node,
                layer_name2node[layer.layer_name],
                label=f"{edge_name}\\l{input_type}\\l",
            )
        )
