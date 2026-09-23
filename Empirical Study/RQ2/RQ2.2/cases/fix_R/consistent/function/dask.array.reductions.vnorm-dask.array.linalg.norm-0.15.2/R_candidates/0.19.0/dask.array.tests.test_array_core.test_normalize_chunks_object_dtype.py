@pytest.mark.parametrize('dtype', [object, [('a', object), ('b', int)]])
def test_normalize_chunks_object_dtype(dtype):
    x = np.array(['a', 'abc'], dtype=object)
    with pytest.raises(NotImplementedError):
        da.from_array(x, chunks='auto')
