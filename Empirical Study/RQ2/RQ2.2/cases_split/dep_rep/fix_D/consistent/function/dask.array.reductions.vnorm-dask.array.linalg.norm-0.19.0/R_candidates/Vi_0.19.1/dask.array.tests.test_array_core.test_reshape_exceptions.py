def test_reshape_exceptions():
    x = np.random.randint(10, size=(5,))
    a = from_array(x, chunks=(2,))
    with pytest.raises(ValueError):
        da.reshape(a, (100,))
