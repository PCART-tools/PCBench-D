@register_meta(aten._jagged_to_padded_dense_forward.default)
def meta__jagged_to_padded_dense_forward(
    values: Tensor,
    offsets: list[Tensor],
    max_lengths: list[int],
    padding_value: float = 0.0,
):
    # only one jagged dim is supported for now
    assert len(offsets) == 1
    assert len(max_lengths) == 1

    B = offsets[0].shape[0] - 1
    S = max_lengths[0]
    output_shape = (B, S, *values.shape[1:])
    return values.new_empty(output_shape)
