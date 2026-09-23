def test_enzo_example_c_with_degeneracy():
    # rescued from https://github.com/scipy/scipy/pull/218
    m = 20
    c = -np.ones(m)
    tmp = 2*np.pi*np.arange(1, m+1)/(m+1)
    A_eq = np.vstack((np.cos(tmp)-1, np.sin(tmp)))
    b_eq = [0, 0]
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq)
    _assert_success(res, desired_fun=0, desired_x=np.zeros(m))
