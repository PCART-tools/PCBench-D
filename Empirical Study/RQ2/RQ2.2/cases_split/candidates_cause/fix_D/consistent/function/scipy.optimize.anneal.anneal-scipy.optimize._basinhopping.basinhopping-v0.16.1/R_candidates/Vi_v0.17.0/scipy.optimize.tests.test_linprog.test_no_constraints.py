def test_no_constraints():
    res = linprog([-1, -2])
    assert_equal(res.x, [0, 0])
    _assert_unbounded(res)
