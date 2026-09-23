def test_round():
    x = np.random.random(10)
    d = da.from_array(x, chunks=4)

    for i in (0, 1, 4, 5):
        assert_eq(x.round(i), d.round(i))

    assert_eq(d.round(2), da.round(d, 2))
