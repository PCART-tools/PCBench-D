def test_slice_dtype(dtype, index):
    result = _make_sliced_dtype(dtype, index)
    expected = np.ones((5, len(dtype)), dtype=dtype)[index].dtype
    assert result == expected
