def sample_inputs_rsub(op_info, device, dtype, requires_grad, other_scalar, **kwargs):
    make_arg = partial(make_tensor, device=device)

    shapes = ((S, S), (S,), ()) if not other_scalar else ((),)
    # We are doing y - a*x, where y may be a scalar or a tensor
    # If y is a scalar, y may be of any dtype that can be cast to the dtype of x
    # a may always be of any dtype that can be cast to the dtype of x
    if dtype.is_complex:
        dtypes_a = (torch.int32, torch.float32, dtype)
    elif dtype.is_floating_point:
        dtypes_a = (torch.int32, dtype)
    else:
        dtypes_a = (dtype, )
    dtypes_y = dtypes_a if other_scalar else (dtype,)

    for shape_x, shape_y, dtype_y, dtype_a in product(shapes, shapes, dtypes_y, dtypes_a):
        requires_grad_y = (requires_grad and
                           not other_scalar and
                           (dtype_y.is_floating_point or dtype_y.is_complex))

        x = make_arg(shape_x, dtype=dtype, requires_grad=requires_grad)
        y = make_arg(shape_y, dtype=dtype_y, requires_grad=requires_grad_y)
        if other_scalar:
            y = y.item()
        a = make_arg((), dtype=dtype_a).item()
        yield SampleInput(x, args=(y,), kwargs={"alpha": a})
