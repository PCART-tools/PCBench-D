def visualize_min_cut_graph(nx_graph):
    import networkx as nx
    import pydot

    dot_format = nx.nx_pydot.to_pydot(nx_graph).to_string()
    dot_graph = pydot.graph_from_dot_data(dot_format)[0]  # type: ignore[index]
    for edge in dot_graph.get_edges():
        weight = nx_graph[edge.get_source()][edge.get_destination()]["capacity"]
        # Set edge label to weight
        edge.set_label(str(weight))  # type: ignore[union-attr]
        # Color edges with weight 'inf' as red
        if weight == float("inf"):
            edge.set_color("red")  # type: ignore[union-attr]
    log.info("Visualizing the failed graph to min_cut_failed.svg")
    dot_graph.write_svg("min_cut_failed.svg")  # type: ignore[union-attr]
