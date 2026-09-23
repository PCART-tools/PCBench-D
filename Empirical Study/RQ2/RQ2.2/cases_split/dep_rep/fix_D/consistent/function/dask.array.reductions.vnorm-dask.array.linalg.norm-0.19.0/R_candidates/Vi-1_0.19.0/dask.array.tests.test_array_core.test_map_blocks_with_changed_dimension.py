def test_map_blocks_with_changed_dimension():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(7, 4))

    e = d.map_blocks(lambda b: b.sum(axis=0), chunks=(4,), drop_axis=0,
                     dtype=d.dtype)
    assert e.chunks == ((4, 4),)
    assert_eq(e, x.sum(axis=0))

    # Provided chunks have wrong shape
    with pytest.raises(ValueError):
        d.map_blocks(lambda b: b.sum(axis=0), chunks=(7, 4), drop_axis=0)

    with pytest.raises(ValueError):
        d.map_blocks(lambda b: b.sum(axis=0), chunks=((4, 4, 4),), drop_axis=0)

    # Can't drop axis with more than 1 block
    with pytest.raises(ValueError):
        d.map_blocks(lambda b: b.sum(axis=1), drop_axis=1, dtype=d.dtype)

    # Adding axis with a gap
    with pytest.raises(ValueError):
        d.map_blocks(lambda b: b, new_axis=(3, 4))

    d = da.from_array(x, chunks=(4, 8))
    e = d.map_blocks(lambda b: b.sum(axis=1), drop_axis=1, dtype=d.dtype)
    assert e.chunks == ((4, 3),)
    assert_eq(e, x.sum(axis=1))

    x = np.arange(64).reshape((8, 8))
    d = da.from_array(x, chunks=(4, 4))
    e = d.map_blocks(lambda b: b[None, :, :, None],
                     chunks=(1, 4, 4, 1), new_axis=[0, 3], dtype=d.dtype)
    assert e.chunks == ((1,), (4, 4), (4, 4), (1,))
    assert_eq(e, x[None, :, :, None])

    e = d.map_blocks(lambda b: b[None, :, :, None],
                     new_axis=[0, 3], dtype=d.dtype)
    assert e.chunks == ((1,), (4, 4), (4, 4), (1,))
    assert_eq(e, x[None, :, :, None])

    # Both new_axis and drop_axis
    d = da.from_array(x, chunks=(8, 4))
    e = d.map_blocks(lambda b: b.sum(axis=0)[:, None, None],
                     drop_axis=0, new_axis=(1, 2), dtype=d.dtype)
    assert e.chunks == ((4, 4), (1,), (1,))
    assert_eq(e, x.sum(axis=0)[:, None, None])

    d = da.from_array(x, chunks=(4, 8))
    e = d.map_blocks(lambda b: b.sum(axis=1)[:, None, None],
                     drop_axis=1, new_axis=(1, 2), dtype=d.dtype)
    assert e.chunks == ((4, 4), (1,), (1,))
    assert_eq(e, x.sum(axis=1)[:, None, None])
