def test_indices_no_chunks():
    with pytest.raises(ValueError):
        da.indices((1,))
