def test_oob_check():
    x = da.ones(5, chunks=(2,))
    with pytest.raises(IndexError):
        x[6]
    with pytest.raises(IndexError):
        x[[6]]
