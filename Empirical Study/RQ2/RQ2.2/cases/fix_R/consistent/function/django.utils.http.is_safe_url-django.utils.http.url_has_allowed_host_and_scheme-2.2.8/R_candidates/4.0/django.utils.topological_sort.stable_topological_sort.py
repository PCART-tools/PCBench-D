def stable_topological_sort(nodes, dependency_graph):
    result = []
    for layer in topological_sort_as_sets(dependency_graph):
        for node in nodes:
            if node in layer:
                result.append(node)
    return result
