def get_all_graph_pipes(graph):
    results = set()
    for datapipe, sub_graph in graph.items():
        results.add(datapipe)
        sub_items = get_all_graph_pipes(sub_graph)
        for item in sub_items:
            results.add(item)
    return results
