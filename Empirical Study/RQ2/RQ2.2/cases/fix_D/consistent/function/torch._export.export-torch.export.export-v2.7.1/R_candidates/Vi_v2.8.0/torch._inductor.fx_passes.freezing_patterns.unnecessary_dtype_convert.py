@register_graph_pattern(
    CallFunction(
        torch.ops.prims.convert_element_type.default,
        Ignored(),
        KeywordArg("dtype"),
    ),
    pass_dict=pass_patterns[0],
    extra_check=same_dtype,
)
def unnecessary_dtype_convert(match: Match, **kwargs):
    """Remove unnecessary dtype conversion op, probably left as a result of Conv-Bn folding"""
    graph = match.graph
    node = match.output_node()
    node.replace_all_uses_with(node.args[0])  # type: ignore[arg-type]
    graph.erase_node(node)
