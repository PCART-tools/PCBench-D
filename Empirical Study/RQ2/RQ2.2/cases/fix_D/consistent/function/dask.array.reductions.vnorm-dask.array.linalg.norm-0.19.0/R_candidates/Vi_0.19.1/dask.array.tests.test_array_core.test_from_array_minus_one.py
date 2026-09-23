def test_from_array_minus_one():
    x = np.arange(10)
    y = da.from_array(x, -1)
    assert y.chunks == ((10,),)
    assert_eq(x, y)
