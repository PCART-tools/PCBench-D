def validate_grid_path(r, c, s, t, p):
    ok_(isinstance(p, list))
    assert_equal(p[0], s)
    assert_equal(p[-1], t)
    s = ((s - 1) // c, (s - 1) % c)
    t = ((t - 1) // c, (t - 1) % c)
    assert_equal(len(p), abs(t[0] - s[0]) + abs(t[1] - s[1]) + 1)
    p = [((u - 1) // c, (u - 1) % c) for u in p]
    for u in p:
        ok_(0 <= u[0] < r)
        ok_(0 <= u[1] < c)
    for u, v in zip(p[:-1], p[1:]):
        ok_((abs(v[0] - u[0]), abs(v[1] - u[1])) in [(0, 1), (1, 0)])
