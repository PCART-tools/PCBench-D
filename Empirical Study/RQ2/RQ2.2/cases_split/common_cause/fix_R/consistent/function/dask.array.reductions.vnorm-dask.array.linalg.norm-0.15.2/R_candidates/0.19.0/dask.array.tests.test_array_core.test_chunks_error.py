def test_chunks_error():
    x = np.ones((10, 10))
    with pytest.raises(ValueError):
        da.from_array(x, chunks=(5,))
