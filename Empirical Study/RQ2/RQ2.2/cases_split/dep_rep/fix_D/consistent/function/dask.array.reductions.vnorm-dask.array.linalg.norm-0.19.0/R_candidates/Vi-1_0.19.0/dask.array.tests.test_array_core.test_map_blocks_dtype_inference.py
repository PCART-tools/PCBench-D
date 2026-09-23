def test_map_blocks_dtype_inference():
    x = np.arange(50).reshape((5, 10))
    y = np.arange(10)
    dx = da.from_array(x, chunks=5)
    dy = da.from_array(y, chunks=5)

    def foo(x, *args, **kwargs):
        cast = kwargs.pop('cast', 'i8')
        return (x + sum(args)).astype(cast)

    assert_eq(dx.map_blocks(foo, dy, 1), foo(dx, dy, 1))
    assert_eq(dx.map_blocks(foo, dy, 1, cast='f8'), foo(dx, dy, 1, cast='f8'))
    assert_eq(dx.map_blocks(foo, dy, 1, cast='f8', dtype='f8'),
              foo(dx, dy, 1, cast='f8', dtype='f8'))

    def foo(x):
        raise RuntimeError("Woops")

    try:
        dx.map_blocks(foo)
    except Exception as e:
        assert e.args[0].startswith("`dtype` inference failed")
        assert "Please specify the dtype explicitly" in e.args[0]
        assert 'RuntimeError' in e.args[0]
    else:
        assert False, "Should have errored"
