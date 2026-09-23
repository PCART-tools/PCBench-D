@compatibility(is_backward_compatible=False)
def get_graph_provenance_json(graph: Graph) -> dict[str, Any]:
    """
    Given an fx.Graph, return a json that contains the provenance information of each node.
    """
    provenance_tracking_json = {}
    for node in graph.nodes:
        if node.op == "call_function":
            provenance_tracking_json[node.name] = (
                [source.to_dict() for source in node.meta["from_node"]]
                if "from_node" in node.meta
                else []
            )
    return provenance_tracking_json
