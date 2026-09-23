@pytest.mark.parametrize("funcname, kwargs", [
    ("flipud", {}),
    ("fliplr", {}),
    ("flip", {"axis": 0}),
    ("flip", {"axis": 1}),
    ("flip", {"axis": 2}),
    ("flip", {"axis": -1}),
])
@pytest.mark.parametrize("shape", [
    tuple(),
    (4,),
    (4, 6),
    (4, 6, 8),
    (4, 6, 8, 10),
])
def test_flip(funcname, kwargs, shape):
    if (funcname == "flip" and
            LooseVersion(np.__version__) < LooseVersion("1.12.0")):
        pytest.skip(
            "NumPy %s doesn't support `flip`."
            " Need NumPy 1.12.0 or greater." % np.__version__
        )

    axis = kwargs.get("axis")
    if axis is None:
        if funcname == "flipud":
            axis = 0
        elif funcname == "fliplr":
            axis = 1

    np_a = np.random.random(shape)
    da_a = da.from_array(np_a, chunks=1)

    np_func = getattr(np, funcname)
    da_func = getattr(da, funcname)

    try:
        range(np_a.ndim)[axis]
    except IndexError:
        with pytest.raises(ValueError):
            da_func(da_a, **kwargs)
    else:
        np_r = np_func(np_a, **kwargs)
        da_r = da_func(da_a, **kwargs)

        assert_eq(np_r, da_r)
