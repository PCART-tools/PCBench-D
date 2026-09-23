def test_is_string_like():
    assert is_string_like("aaaa")
    assert not is_string_like(None)
    assert not is_string_like(123)
