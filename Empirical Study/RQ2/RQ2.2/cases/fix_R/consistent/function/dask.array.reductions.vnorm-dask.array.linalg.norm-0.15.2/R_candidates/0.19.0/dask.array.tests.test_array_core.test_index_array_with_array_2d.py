def test_index_array_with_array_2d():
    x = np.arange(24).reshape((4, 6))
    dx = da.from_array(x, chunks=(2, 2))
    dx._chunks = ((2, 2), (np.nan, np.nan, np.nan))

    assert (sorted(x[x % 2 == 0].tolist()) ==
            sorted(dx[dx % 2 == 0].compute().tolist()))
    assert (sorted(x[x > 6].tolist()) ==
            sorted(dx[dx > 6].compute().tolist()))
