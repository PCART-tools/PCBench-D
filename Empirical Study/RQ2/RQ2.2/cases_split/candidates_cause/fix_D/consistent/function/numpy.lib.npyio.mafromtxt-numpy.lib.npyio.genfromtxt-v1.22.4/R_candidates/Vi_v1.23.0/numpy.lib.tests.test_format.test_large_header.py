def test_large_header():
    s = BytesIO()
    d = {'a': 1, 'b': 2}
    format.write_array_header_1_0(s, d)

    s = BytesIO()
    d = {'a': 1, 'b': 2, 'c': 'x'*256*256}
    assert_raises(ValueError, format.write_array_header_1_0, s, d)
