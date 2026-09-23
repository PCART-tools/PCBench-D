def reduction_1d_test(da_func, darr, np_func, narr, use_dtype=True, split_every=True):
    assert_eq(da_func(darr), np_func(narr))
    assert_eq(da_func(darr, keepdims=True), np_func(narr, keepdims=True))
    assert same_keys(da_func(darr), da_func(darr))
    assert same_keys(da_func(darr, keepdims=True), da_func(darr, keepdims=True))
    if use_dtype:
        assert_eq(da_func(darr, dtype='f8'), np_func(narr, dtype='f8'))
        assert_eq(da_func(darr, dtype='i8'), np_func(narr, dtype='i8'))
        assert same_keys(da_func(darr, dtype='i8'), da_func(darr, dtype='i8'))
    if split_every:
        a1 = da_func(darr, split_every=2)
        a2 = da_func(darr, split_every={0: 2})
        assert same_keys(a1, a2)
        assert_eq(a1, np_func(narr))
        assert_eq(a2, np_func(narr))
        assert_eq(da_func(darr, keepdims=True, split_every=2),
                  np_func(narr, keepdims=True))
