def test_index_array_with_array_1d():
    x = np.arange(10)
    dx = da.from_array(x, chunks=(5,))
    dx._chunks = ((np.nan, np.nan),)

    assert_eq(x[x > 6], dx[dx > 6])
    assert_eq(x[x % 2 == 0], dx[dx % 2 == 0])

    dy = da.ones(11, chunks=(3,))

    with pytest.raises(ValueError):
        dx[dy > 5]
