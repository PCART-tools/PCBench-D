def _attention_scale(query: TFloat, op: Opset) -> TFloat:
    """Calculate the scale factor for the attention result.

    Args:
        query: Tensor of shape [..., L, E]

    Returns:
        Scalar scale factor := 1 / math.sqrt(query.size(-1))
    """
    q_shape = op.Shape(query)
    q_last_dim = op.Gather(q_shape, op.Constant(value_ints=[-1]))
    embedding_size = op.CastLike(q_last_dim, query)
    one = op.Constant(value_float=1.0)
    cast_one = op.CastLike(one, query)
    scale = op.Div(cast_one, op.Sqrt(embedding_size))
    return scale
