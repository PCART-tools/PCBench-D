@register_op_impl([aten.convolution.default, aten.convolution_backward.default])
def conv(fake_mode, func, *args, **kwargs):
    _, kwargs = normalize_function(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    device = kwargs["input"].fake_device
    # need to re-enable mode so the tensors report fake device
    with fake_mode:
        # if the input is unsqueezed is done in Convolution.cpp we get segfault
        k = kwargs["weight"].ndim
        batch = kwargs["input"].shape[0]

        # Avoid importing sympy at a module level
        from torch.fx.experimental.symbolic_shapes import has_hint

        if not has_hint(batch):
            # TODO: We can make this a little more faithful with best effort
            # channels last detection (but only if it's statically obvious!)
            mem_fmt = None
        elif k == 3 and not kwargs["input"].is_mkldnn and not kwargs["input"].is_xpu:
            mem_fmt = None
        else:
            if func is aten.convolution.default:
                conv_backend = torch._C._select_conv_backend(**kwargs)
            else:
                conv_backend = torch._C._select_conv_backend(
                    kwargs["input"],
                    kwargs["weight"],
                    bias=None,
                    stride=kwargs["stride"],
                    padding=kwargs["padding"],
                    dilation=kwargs["dilation"],
                    transposed=kwargs["transposed"],
                    output_padding=kwargs["output_padding"],
                    groups=kwargs["groups"],
                    bias_sizes=kwargs["bias_sizes"],
                )
            mem_fmt = torch._C._conv_determine_backend_memory_format(
                kwargs["input"], kwargs["weight"], conv_backend
            )

    def convert(t, mem_fmt):
        if t is None:
            return t
        if mem_fmt is not None:
            t = t.to(memory_format=mem_fmt)
        return FakeTensor(fake_mode, t, device)

    with in_kernel_invocation_manager(fake_mode):
        out = func(**kwargs)

        if func is aten.convolution.default:
            return convert(out, mem_fmt)
        else:
            return (
                convert(out[0], mem_fmt),
                convert(out[1], mem_fmt),
                convert(out[2], None),
            )
