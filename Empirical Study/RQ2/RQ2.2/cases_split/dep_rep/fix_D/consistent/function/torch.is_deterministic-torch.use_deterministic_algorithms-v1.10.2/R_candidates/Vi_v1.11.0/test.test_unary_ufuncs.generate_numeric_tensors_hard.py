def generate_numeric_tensors_hard(device, dtype, *,
                                  domain=(None, None),
                                  filter_=None):
    is_signed_integral = dtype in (torch.int8, torch.int16, torch.int32, torch.int64)
    if not (dtype.is_floating_point or dtype.is_complex or is_signed_integral):
        return ()

    if dtype.is_floating_point:
        if dtype is torch.float16:
            # float16 has smaller range.
            vals = _large_float16_vals
        else:
            vals = _large_float_vals
    elif dtype.is_complex:
        vals = tuple(complex(x, y) for x, y in chain(product(_large_float_vals, _large_float_vals),
                                                     product(_float_vals, _large_float_vals),
                                                     product(_large_float_vals, _float_vals)))
    else:
        vals = _large_int_vals

    return generate_tensors_from_vals(vals, device, dtype, domain, filter_)
