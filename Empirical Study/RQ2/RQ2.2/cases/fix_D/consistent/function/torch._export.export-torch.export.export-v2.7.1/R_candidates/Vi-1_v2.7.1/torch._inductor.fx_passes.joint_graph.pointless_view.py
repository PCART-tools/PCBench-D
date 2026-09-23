@register_graph_pattern(
    CallFunction(torch.ops.aten.view.default, KeywordArg("arg"), KeywordArg("size")),
    pass_dict=patterns,
)
def pointless_view(match: Match, arg, size):
    """Remove no-op view"""
    node = match.output_node()
    arg_size = list(node.args[0].meta["val"].shape)  # type: ignore[union-attr]
    if _guard_sizes_oblivious(size, arg_size):
        node.replace_all_uses_with(node.args[0])  # type: ignore[arg-type]
        match.erase_nodes()
