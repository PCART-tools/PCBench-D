def test_from_array_raises_on_bad_chunks():
    x = np.ones(10)

    with pytest.raises(ValueError):
        da.from_array(x, chunks=(5, 5, 5))

    # with pytest.raises(ValueError):
    #      da.from_array(x, chunks=100)

    with pytest.raises(ValueError):
        da.from_array(x, chunks=((5, 5, 5),))
