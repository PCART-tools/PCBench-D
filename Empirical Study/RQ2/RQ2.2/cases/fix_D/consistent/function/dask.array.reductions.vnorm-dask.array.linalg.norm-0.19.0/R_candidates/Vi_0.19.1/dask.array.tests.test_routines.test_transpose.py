def test_transpose():
    x = np.arange(240).reshape((4, 6, 10))
    d = da.from_array(x, (2, 3, 4))

    assert_eq(d.transpose((2, 0, 1)),
              x.transpose((2, 0, 1)))
    assert same_keys(d.transpose((2, 0, 1)), d.transpose((2, 0, 1)))

    assert_eq(d.transpose(2, 0, 1),
              x.transpose(2, 0, 1))
    assert same_keys(d.transpose(2, 0, 1), d.transpose(2, 0, 1))

    with pytest.raises(ValueError):
        d.transpose(1, 2)

    with pytest.raises(ValueError):
        d.transpose((1, 2))
