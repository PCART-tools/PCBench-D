def test_simple_bounds():
    res = linprog([1, 2], bounds=(1, 2))
    _assert_success(res, desired_x=[1, 1])
    res = linprog([1, 2], bounds=[(1, 2), (1, 2)])
    _assert_success(res, desired_x=[1, 1])
