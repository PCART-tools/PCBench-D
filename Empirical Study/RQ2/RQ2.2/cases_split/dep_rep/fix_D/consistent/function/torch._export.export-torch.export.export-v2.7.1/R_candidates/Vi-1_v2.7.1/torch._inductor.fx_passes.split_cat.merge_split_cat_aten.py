@register_graph_pattern(
    CallFunction(
        torch.ops.aten.cat.default,
        getitem_split_aten,
        dim=Ignored(),
        _users=MULTIPLE,
    ),
    pass_dict=construct_pattern_matcher_pass("split_cat_aten_pass"),
)
def merge_split_cat_aten(match: Match, *args, **kwargs):
    graph = match.graph
    split_node = match.nodes[0]
    split_input, _, split_dim = _get_split_args_default(split_node)
    # get the getitem nodes from the split node
    getitem_nodes = list(split_node.users.keys())
    for cat_node in list(getitem_nodes[0].users.keys()):
        cat_dim = get_arg_value(cat_node, 1, "dim")
        cat_inputs = get_arg_value(cat_node, 0, "tensors")
        # check split node and cat node has same dim, and all getitem nodes have same parent node
        if split_dim != cat_dim or not has_same_parent_node(cat_node):
            continue
        # check the cat node has consecutive indices
        indices = [arg.args[1] for arg in cat_node.args[0]]  # type: ignore[union-attr]
        if (
            not is_sorted_and_consecutive(indices)  # type: ignore[arg-type]
            and len(getitem_nodes) != len(cat_inputs)
        ):
            continue
        # replace the users of the cat node to be the input of the split node
        cat_node.replace_all_uses_with(split_input)
        # remove the cat node
        graph.erase_node(cat_node)
        # remove getitem nodes and split node with no users
        for getitem_node in getitem_nodes:
            if len(getitem_node.users) == 0:
                graph.erase_node(getitem_node)
        if len(split_node.users) == 0:
            graph.erase_node(split_node)
        counters["inductor"]["split_cat_aten_pass"] += 1
