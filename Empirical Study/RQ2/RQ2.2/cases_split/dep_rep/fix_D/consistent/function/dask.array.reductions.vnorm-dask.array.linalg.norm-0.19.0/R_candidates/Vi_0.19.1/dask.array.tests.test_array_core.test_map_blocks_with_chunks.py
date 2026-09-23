def test_map_blocks_with_chunks():
    dx = da.ones((5, 3), chunks=(2, 2))
    dy = da.ones((5, 3), chunks=(2, 2))
    dz = da.map_blocks(np.add, dx, dy, chunks=dx.chunks)
    assert_eq(dz, np.ones((5, 3)) * 2)
