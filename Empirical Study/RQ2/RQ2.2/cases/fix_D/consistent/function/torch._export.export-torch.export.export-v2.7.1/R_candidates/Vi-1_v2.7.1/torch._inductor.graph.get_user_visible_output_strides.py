def get_user_visible_output_strides(g: Graph) -> dict[Node, tuple[int, ...]]:
    ret: dict[Node, tuple[int, ...]] = {}
    output_node = g.find_nodes(op="output")[0]

    if "user_visible_output_idxs" not in output_node.meta:
        return ret

    for idx, node in enumerate(output_node.args[0]):
        if idx in output_node.meta["user_visible_output_idxs"]:
            ret[node] = output_node.meta["original_output_strides"][idx]
    return ret
