@register_op_impl(torch.ops.aten._pack_padded_sequence.default)
def _pack_padded_sequence(fake_mode, func, inputs, lengths, batch_first):
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    new_batch_size = fake_mode.shape_env.create_unbacked_symint()

    from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

    _constrain_range_for_size(new_batch_size)

    if not batch_first:
        # Inputs should have shape (batch_size, seq_len, *)
        inputs = inputs.transpose(0, 1)

    res_size = inputs.shape[1:]
    packed_data = inputs.new_empty(res_size)
    batch_size = inputs.new_empty((new_batch_size,))
    return (packed_data, batch_size)
