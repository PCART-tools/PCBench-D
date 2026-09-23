@register_op_impl(aten.repeat_interleave.Tensor)
def repeat_interleave_tensor(fake_mode, func, repeats, output_size=None):
    if output_size is None:
        if (
            fake_mode.shape_env is None
            or not fake_mode.shape_env.allow_dynamic_output_shape_ops
        ):
            raise DynamicOutputShapeException(func)

        output_size = fake_mode.shape_env.create_unbacked_symint()

        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

        _constrain_range_for_size(output_size)
        # TODO: consider a memo
    return repeats.new_empty(output_size)
