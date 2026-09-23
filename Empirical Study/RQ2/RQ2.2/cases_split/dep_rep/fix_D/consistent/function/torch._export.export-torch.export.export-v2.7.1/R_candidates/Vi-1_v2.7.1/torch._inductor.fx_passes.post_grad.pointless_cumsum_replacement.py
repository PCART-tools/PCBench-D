@register_graph_pattern(
    CallFunction(
        aten.cumsum.default,
        CallFunction(
            torch.ops.aten.full.default,
            KeywordArg("shape"),
            KeywordArg("fill_value"),
            dtype=KeywordArg("dtype"),
            layout=Ignored(),
            device=KeywordArg("device"),
            pin_memory=False,
            _users=MULTIPLE,
        ),
        KeywordArg("dim"),
        _users=MULTIPLE,
    ),
    pass_dict=pass_patterns[1],
)
def pointless_cumsum_replacement(match: Match, shape, fill_value, device, dtype, dim):
    """Based on a pattern in OPTForCausalLM"""

    if is_integer_dtype(dtype) or is_boolean_dtype(dtype):
        # cumsum promotes all integral types to int64
        dtype = torch.int64

    def repl(*shape):
        dim_size = shape[dim]
        idx = torch.arange(1, dim_size + 1, device=device, dtype=dtype)

        inter_shape = [1] * len(shape)
        inter_shape[dim] = dim_size
        return (idx * fill_value).view(inter_shape).expand(shape)

    # only replace the output node, not all nodes
    match.nodes = [match.output_node()]
    match.replace_by_example(repl, list(shape))
