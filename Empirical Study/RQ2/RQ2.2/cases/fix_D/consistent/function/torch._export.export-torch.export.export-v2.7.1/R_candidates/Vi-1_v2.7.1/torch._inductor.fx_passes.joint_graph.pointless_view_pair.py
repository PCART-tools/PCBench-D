@register_graph_pattern(
    CallFunction(
        aten.view.default,
        CallFunction(aten.view.default, KeywordArg("arg"), KeywordArg("size1")),
        KeywordArg("size2"),
    ),
    pass_dict=patterns,
)
def pointless_view_pair(match: Match, arg, size1, size2):
    """
    Remove a pair of views that are pointless.
    """
    node = match.output_node()
    arg_size = list(arg.meta["val"].shape)
    if _guard_sizes_oblivious(arg_size, size2):
        node.replace_all_uses_with(arg)
        match.erase_nodes()
