def _get_output_nodes(g: Graph) -> List[Node]:
    return [n for n in g.nodes if n.op == 'output']
