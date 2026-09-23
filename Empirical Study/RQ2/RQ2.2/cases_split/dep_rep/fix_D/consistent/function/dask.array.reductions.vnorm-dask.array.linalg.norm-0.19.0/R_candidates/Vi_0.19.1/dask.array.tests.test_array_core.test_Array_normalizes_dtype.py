def test_Array_normalizes_dtype():
    x = da.ones((3,), chunks=(1,), dtype=int)
    assert isinstance(x.dtype, np.dtype)
