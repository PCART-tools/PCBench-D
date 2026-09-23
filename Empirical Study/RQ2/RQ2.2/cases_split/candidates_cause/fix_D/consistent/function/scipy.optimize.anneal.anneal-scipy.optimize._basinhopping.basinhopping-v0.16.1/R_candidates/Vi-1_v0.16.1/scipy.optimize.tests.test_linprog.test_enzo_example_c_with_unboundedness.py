def test_enzo_example_c_with_unboundedness():
    # rescued from https://github.com/scipy/scipy/pull/218
    m = 50
    c = -np.ones(m)
    tmp = 2*np.pi*np.arange(m)/(m+1)
    A_eq = np.vstack((np.cos(tmp)-1, np.sin(tmp)))
    b_eq = [0, 0]
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq)
    _assert_unbounded(res)
