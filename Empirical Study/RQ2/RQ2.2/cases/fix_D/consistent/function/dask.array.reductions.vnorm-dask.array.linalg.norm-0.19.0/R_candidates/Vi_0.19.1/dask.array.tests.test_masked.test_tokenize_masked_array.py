def test_tokenize_masked_array():
    m = np.ma.masked_array([1, 2, 3], mask=[True, True, False], fill_value=10)
    m2 = np.ma.masked_array([1, 2, 3], mask=[True, True, False], fill_value=0)
    m3 = np.ma.masked_array([1, 2, 3], mask=False, fill_value=10)
    assert tokenize(m) == tokenize(m)
    assert tokenize(m2) == tokenize(m2)
    assert tokenize(m3) == tokenize(m3)
    assert tokenize(m) != tokenize(m2)
    assert tokenize(m) != tokenize(m3)
