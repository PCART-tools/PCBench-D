@pytest.mark.parametrize(
    "funcname", [
        "empty_like", "empty",
        "ones_like", "ones",
        "zeros_like", "zeros",
        "full_like", "full",
    ]
)
@pytest.mark.parametrize("cast_shape", [tuple, list, np.asarray])
@pytest.mark.parametrize("cast_chunks", [tuple, list, np.asarray])
@pytest.mark.parametrize(
    "shape, chunks", [
        ((10, 10), (4, 4))
    ]
)
@pytest.mark.parametrize(
    "dtype", [
        "i4",
    ]
)
def test_arr_like(funcname, shape, cast_shape, dtype, cast_chunks, chunks):
    np_func = getattr(np, funcname)
    da_func = getattr(da, funcname)
    shape = cast_shape(shape)
    chunks = cast_chunks(chunks)

    if "full" in funcname:
        old_np_func = np_func
        old_da_func = da_func

        np_func = lambda *a, **k: old_np_func(*a, fill_value=5, **k)
        da_func = lambda *a, **k: old_da_func(*a, fill_value=5, **k)

    dtype = np.dtype(dtype)

    if "like" in funcname:
        a = np.random.randint(0, 10, shape).astype(dtype)

        np_r = np_func(a)
        da_r = da_func(a, chunks=chunks)
    else:
        np_r = np_func(shape, dtype=dtype)
        da_r = da_func(shape, dtype=dtype, chunks=chunks)

    assert np_r.shape == da_r.shape
    assert np_r.dtype == da_r.dtype

    if "empty" not in funcname:
        assert (np_r == np.asarray(da_r)).all()
