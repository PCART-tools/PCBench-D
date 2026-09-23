@register_op_impl(
    lambda func: torch.Tag.dynamic_output_shape in func.tags
    and func
    not in [aten.index.Tensor, aten.nonzero.default, aten.repeat_interleave.Tensor]
)
def dyn_shape(fake_mode, func, *args, **kwargs):
    raise DynamicOutputShapeException(func)
