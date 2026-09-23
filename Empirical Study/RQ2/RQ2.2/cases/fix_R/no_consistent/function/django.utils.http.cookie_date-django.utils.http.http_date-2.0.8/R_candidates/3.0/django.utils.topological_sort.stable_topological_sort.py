def stable_topological_sort(l, dependency_graph):
    result = []
    for layer in topological_sort_as_sets(dependency_graph):
        for node in l:
            if node in layer:
                result.append(node)
    return result
