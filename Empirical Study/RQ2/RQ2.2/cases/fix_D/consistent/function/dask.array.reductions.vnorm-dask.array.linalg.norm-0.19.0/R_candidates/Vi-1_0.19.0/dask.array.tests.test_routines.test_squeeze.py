@pytest.mark.parametrize('is_func', [True, False])
@pytest.mark.parametrize('axis', [None, 0, -1, (0, -1)])
def test_squeeze(is_func, axis):
    a = np.arange(10)[None, :, None, None]
    d = da.from_array(a, chunks=(1, 3, 1, 1))

    if is_func:
        a_s = np.squeeze(a, axis=axis)
        d_s = da.squeeze(d, axis=axis)
    else:
        a_s = a.squeeze(axis=axis)
        d_s = d.squeeze(axis=axis)

    assert_eq(d_s, a_s)
    assert same_keys(d_s, da.squeeze(d, axis=axis))

    if axis is None:
        axis = tuple(range(a.ndim))
    else:
        axis = axis if isinstance(axis, tuple) else (axis,)
        axis = tuple(i % a.ndim for i in axis)
    axis = tuple(
        i for i, c in enumerate(d.chunks) if i in axis and len(c) == 1
    )

    exp_d_s_chunks = tuple(
        c for i, c in enumerate(d.chunks) if i not in axis
    )
    assert d_s.chunks == exp_d_s_chunks
