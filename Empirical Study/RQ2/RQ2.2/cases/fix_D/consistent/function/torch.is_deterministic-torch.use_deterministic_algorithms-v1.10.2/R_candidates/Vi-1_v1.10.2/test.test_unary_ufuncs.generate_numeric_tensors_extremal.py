def generate_numeric_tensors_extremal(device, dtype, *,
                                      domain=(None, None)):
    if not (dtype.is_floating_point or dtype.is_complex):
        return ()

    vals = []
    if dtype.is_floating_point:
        vals = _float_extremals
    elif dtype.is_complex:
        vals = tuple(complex(x, y) for x, y in chain(product(_float_extremals, _float_extremals),
                                                     product(_float_vals, _float_extremals),
                                                     product(_float_extremals, _float_vals)))

    return generate_tensors_from_vals(vals, device, dtype, domain)
