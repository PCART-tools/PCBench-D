@register_jagged_func(
    [
        torch.ops.aten.elu_backward.default,
        torch.ops.aten.hardshrink_backward.default,
        torch.ops.aten.hardsigmoid_backward.default,
        torch.ops.aten.hardtanh_backward.default,
        torch.ops.aten.softplus_backward.default,
        torch.ops.aten.softshrink_backward.default,
    ],
    "self: jt_all, ...",
)
def activation_backward(func, *args, **kwargs):
    # first NJT arg is expected to be grad_output
    grad_output = next(arg for arg in args if isinstance(arg, NestedTensor))
    return NestedTensor(
        func(
            *(arg._values if isinstance(arg, NestedTensor) else arg for arg in args),
            **kwargs,
        ),
        **extract_kwargs(grad_output),
    )
