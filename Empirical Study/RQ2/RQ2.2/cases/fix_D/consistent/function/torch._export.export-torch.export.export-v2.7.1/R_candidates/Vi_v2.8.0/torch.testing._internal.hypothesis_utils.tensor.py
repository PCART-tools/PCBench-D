@st.composite
def tensor(draw, shapes=None, elements=None, qparams=None, dtype=np.float32):
    if isinstance(shapes, SearchStrategy):
        _shape = draw(shapes)
    else:
        _shape = draw(st.sampled_from(shapes))
    if qparams is None:
        if elements is None:
            elements = floats(-1e6, 1e6, allow_nan=False, width=32)
        X = draw(stnp.arrays(dtype=dtype, elements=elements, shape=_shape))
        assume(not (np.isnan(X).any() or np.isinf(X).any()))
        return X, None
    qparams = draw(qparams)
    if elements is None:
        min_value, max_value = _get_valid_min_max(qparams)
        elements = floats(min_value, max_value, allow_infinity=False,
                          allow_nan=False, width=32)
    X = draw(stnp.arrays(dtype=dtype, elements=elements, shape=_shape))
    # Recompute the scale and zero_points according to the X statistics.
    scale, zp = _calculate_dynamic_qparams(X, qparams[2])
    enforced_zp = _ENFORCED_ZERO_POINT.get(qparams[2], None)
    if enforced_zp is not None:
        zp = enforced_zp
    return X, (scale, zp, qparams[2])
