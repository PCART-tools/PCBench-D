def reduction_2d_test(da_func, darr, np_func, narr, use_dtype=True,
                      split_every=True):
    assert_eq(da_func(darr), np_func(narr))
    assert_eq(da_func(darr, keepdims=True), np_func(narr, keepdims=True))
    assert_eq(da_func(darr, axis=0), np_func(narr, axis=0))
    assert_eq(da_func(darr, axis=1), np_func(narr, axis=1))
    assert_eq(da_func(darr, axis=-1), np_func(narr, axis=-1))
    assert_eq(da_func(darr, axis=-2), np_func(narr, axis=-2))
    assert_eq(da_func(darr, axis=1, keepdims=True),
              np_func(narr, axis=1, keepdims=True))
    assert_eq(da_func(darr, axis=(1, 0)), np_func(narr, axis=(1, 0)))

    assert same_keys(da_func(darr, axis=1), da_func(darr, axis=1))
    assert same_keys(da_func(darr, axis=(1, 0)), da_func(darr, axis=(1, 0)))

    if use_dtype:
        assert_eq(da_func(darr, dtype='f8'), np_func(narr, dtype='f8'))
        assert_eq(da_func(darr, dtype='i8'), np_func(narr, dtype='i8'))

    if split_every:
        a1 = da_func(darr, split_every=4)
        a2 = da_func(darr, split_every={0: 2, 1: 2})
        assert same_keys(a1, a2)
        assert_eq(a1, np_func(narr))
        assert_eq(a2, np_func(narr))
        assert_eq(da_func(darr, keepdims=True, split_every=4),
                  np_func(narr, keepdims=True))
        assert_eq(da_func(darr, axis=0, split_every=2), np_func(narr, axis=0))
        assert_eq(da_func(darr, axis=0, keepdims=True, split_every=2),
                  np_func(narr, axis=0, keepdims=True))
        assert_eq(da_func(darr, axis=1, split_every=2), np_func(narr, axis=1))
        assert_eq(da_func(darr, axis=1, keepdims=True, split_every=2),
                  np_func(narr, axis=1, keepdims=True))
