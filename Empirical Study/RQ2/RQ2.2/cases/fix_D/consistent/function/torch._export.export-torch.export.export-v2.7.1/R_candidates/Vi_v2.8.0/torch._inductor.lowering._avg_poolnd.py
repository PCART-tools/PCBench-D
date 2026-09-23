def _avg_poolnd(
    x,
    kernel_size,
    stride,
    padding,
    ceil_mode,
    count_include_pad,
    divisor_override,
    dim,
):
    if not stride:
        stride = kernel_size
    if not padding:
        padding = [0] * dim
    kernel_size = pad_listlike(kernel_size, dim)
    stride = pad_listlike(stride, dim)
    padding = pad_listlike(padding, dim)

    assert isinstance(x, TensorBox)
    assert len(kernel_size) == dim
    assert len(stride) == dim
    assert len(padding) == dim
    assert len(x.get_size()) in (dim + 1, dim + 2)

    x.realize_hint()
    batch = x.get_size()[:-dim]
    h = x.get_size()[-dim:]

    h_out, ceil_modes = zip(
        *[
            pooling_size(h[i], i, kernel_size, stride, padding, ceil_mode)
            for i in range(dim)
        ]
    )

    if any(padding) or any(ceil_modes):
        x_loader = constant_boundary_condition(x, 0.0, dim=dim)
        had_padding = True
    else:
        x_loader = x.make_loader()
        had_padding = False

    new_size = list(batch) + list(h_out)
    dtype = x.get_dtype()

    window_size = functools.reduce(operator.mul, kernel_size)
    if window_size > 25:
        # Kernel size too big. Results in hard-to-optimize Triton code. Use fallback.
        if dim == 2:
            fallback = fallback_avg_pool2d
        elif dim == 3:
            fallback = fallback_avg_pool3d
        else:
            raise ValueError(f"Unknown dim: {dim}")

        return fallback(
            x,
            kernel_size,
            stride,
            padding,
            ceil_mode,
            count_include_pad,
            divisor_override,
        )

    def fn_sum(idx, loader):
        prefix = idx[:-dim]
        b = idx[-dim:]
        total = None
        for ih in itertools.product(*[range(kernel_size[i]) for i in range(dim)]):
            inp = [b[i] * stride[i] + ih[i] - padding[i] for i in range(dim)]
            val = loader([*prefix, *inp])
            if total is None:
                total = val
            else:
                total = ops.add(val, total)
        return total

    if not had_padding or divisor_override:
        divisor = divisor_override if divisor_override else window_size
        if dtype.is_floating_point:
            scale = 1 / divisor

            def fn(idx):
                return ops.mul(fn_sum(idx, x_loader), ops.constant(scale, dtype))

        else:

            def fn(idx):
                # C style integer division as done in native/cpu/AvgPoolKernel.cpp
                return ops.truncdiv(fn_sum(idx, x_loader), ops.constant(divisor, dtype))

    else:

        def fn(idx):
            bh = idx[-dim:]

            divide_factors = []
            for i in range(dim):
                hstart = bh[i] * stride[i] - padding[i]
                hend = sympy.Min(hstart + kernel_size[i], h[i] + padding[i])
                if not count_include_pad:
                    hstart = sympy.Max(hstart, 0)
                    hend = sympy.Min(hend, h[i])
                factor = ops.index_expr(hend - hstart, torch.int32)
                divide_factors.append(factor)
            divide_factor = functools.reduce(ops.mul, divide_factors)
            if dtype.is_floating_point:
                return ops.truediv(fn_sum(idx, x_loader), divide_factor)
            # C style integer division as done in native/cpu/AvgPoolKernel.cpp
            return ops.truncdiv(fn_sum(idx, x_loader), divide_factor)

    rv = Pointwise.create(
        device=x.get_device(),
        dtype=dtype,
        inner_fn=fn,
        ranges=new_size,
    )
    # TODO(jansel): should we force these to be realized?
    return rv
