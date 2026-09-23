def test_rechunk_with_null_dimensions():
    x = da.from_array(np.ones((24, 24)), chunks=(4, 8))
    assert (x.rechunk(chunks=(None, 4)).chunks ==
            da.ones((24, 24), chunks=(4, 4)).chunks)
