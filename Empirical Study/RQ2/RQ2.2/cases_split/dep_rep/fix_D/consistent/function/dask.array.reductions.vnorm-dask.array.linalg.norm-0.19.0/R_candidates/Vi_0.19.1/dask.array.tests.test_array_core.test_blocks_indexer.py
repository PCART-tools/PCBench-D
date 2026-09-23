def test_blocks_indexer():
    x = da.arange(10, chunks=2)

    assert isinstance(x.blocks[0], da.Array)

    assert_eq(x.blocks[0], x[:2])
    assert_eq(x.blocks[-1], x[-2:])
    assert_eq(x.blocks[:3], x[:6])
    assert_eq(x.blocks[[0, 1, 2]], x[:6])
    assert_eq(x.blocks[[3, 0, 2]], np.array([6, 7, 0, 1, 4, 5]))

    x = da.random.random((20, 20), chunks=(4, 5))
    assert_eq(x.blocks[0], x[:4])
    assert_eq(x.blocks[0, :3], x[:4, :15])
    assert_eq(x.blocks[:, :3], x[:, :15])

    x = da.ones((40, 40, 40), chunks=(10, 10, 10))
    assert_eq(x.blocks[0, :, 0], np.ones((10, 40, 10)))

    x = da.ones((2, 2), chunks=1)
    with pytest.raises(ValueError):
        x.blocks[[0, 1], [0, 1]]
    with pytest.raises(ValueError):
        x.blocks[np.array([0, 1]), [0, 1]]
    with pytest.raises(ValueError) as info:
        x.blocks[np.array([0, 1]), np.array([0, 1])]
    assert "list" in str(info.value)
    with pytest.raises(ValueError) as info:
        x.blocks[None, :, :]
    assert "newaxis" in str(info.value) and "not supported" in str(info.value)
    with pytest.raises(IndexError) as info:
        x.blocks[100, 100]
