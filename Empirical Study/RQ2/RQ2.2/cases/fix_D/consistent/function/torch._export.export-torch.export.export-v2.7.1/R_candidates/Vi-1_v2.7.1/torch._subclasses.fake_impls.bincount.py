@register_op_impl(torch.ops.aten.bincount.default)
def bincount(fake_mode, func, inputs, weights=None, minlength=0):
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    new_size = fake_mode.shape_env.create_unbacked_symint()

    from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

    _constrain_range_for_size(new_size, min=minlength)
    return inputs.new_empty(new_size)
