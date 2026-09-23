def test_reshape_splat():
    x = da.ones((5, 5), chunks=(2, 2))
    assert_eq(x.reshape((25,)), x.reshape(25))
