def test_indices_wrong_chunks():
    with pytest.raises(ValueError):
        da.indices((1,), chunks=tuple())
