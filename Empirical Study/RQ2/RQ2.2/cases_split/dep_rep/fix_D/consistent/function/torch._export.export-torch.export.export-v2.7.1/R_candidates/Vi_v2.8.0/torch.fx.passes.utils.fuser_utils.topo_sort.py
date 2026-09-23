@compatibility(is_backward_compatible=False)
def topo_sort(nodes: NodeList) -> NodeList:
    # sort nodes according to the topological order
    indegree_map = dict.fromkeys(nodes, 0)
    candidates: SimpleQueue[Node] = SimpleQueue()

    for node in nodes:
        for n in node.all_input_nodes:
            if n in indegree_map:
                indegree_map[node] += 1
        if indegree_map[node] == 0:
            candidates.put(node)

    sorted_nodes: NodeList = []
    while not candidates.empty():
        node = candidates.get()
        sorted_nodes.append(node)

        for n in node.users:
            if n in indegree_map:
                indegree_map[n] -= 1
                if indegree_map[n] == 0:
                    candidates.put(n)

    assert len(nodes) == len(sorted_nodes), (
        "topological sorted nodes doesn't have same length as input nodes"
    )

    return sorted_nodes
