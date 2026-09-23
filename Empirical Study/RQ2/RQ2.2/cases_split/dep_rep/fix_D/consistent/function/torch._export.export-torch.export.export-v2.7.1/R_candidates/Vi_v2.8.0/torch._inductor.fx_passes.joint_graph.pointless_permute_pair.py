@register_graph_pattern(
    CallFunction(
        aten.permute.default,
        CallFunction(aten.permute.default, KeywordArg("arg"), KeywordArg("perm1")),
        KeywordArg("perm2"),
    ),
    pass_dict=patterns,
)
def pointless_permute_pair(match: Match, arg, perm1, perm2):
    rank = len(perm1)
    assert len(perm2) == rank

    for i in range(rank):
        if perm1[perm2[i]] != i:
            return  # bail out
    node = match.output_node()
    node.replace_all_uses_with(arg)
    match.erase_nodes()
