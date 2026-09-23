def test_make_str_with_unicode():
    x = "qualité"
    y = make_str(x)
    assert isinstance(y, str)
    assert len(y) == 7
