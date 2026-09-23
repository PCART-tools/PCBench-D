def test_cases():

    def check_case(values, method, expected):
        r = rankdata(values, method=method)
        assert_array_equal(r, expected)

    for values, method, expected in _cases:
        yield check_case, values, method, expected
