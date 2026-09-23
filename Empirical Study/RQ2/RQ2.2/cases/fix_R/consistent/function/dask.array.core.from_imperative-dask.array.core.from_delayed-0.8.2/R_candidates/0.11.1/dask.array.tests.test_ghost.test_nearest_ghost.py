def test_nearest_ghost():
    a = np.arange(144).reshape(12, 12).astype(float)

    darr = da.from_array(a, chunks=(6, 6))
    garr = ghost(darr, depth={0: 5, 1: 5},
                 boundary={0: 'nearest', 1: 'nearest'})
    tarr = trim_internal(garr, {0: 5, 1: 5})
    assert_array_almost_equal(tarr, a)
