def test_callback():
    # Check that callback is as advertised
    callback_complete = [False]
    last_xk = []

    def cb(xk, **kwargs):
        kwargs.pop('tableau')
        assert_(isinstance(kwargs.pop('phase'), int))
        assert_(isinstance(kwargs.pop('nit'), int))

        i, j = kwargs.pop('pivot')
        assert_(np.isscalar(i))
        assert_(np.isscalar(j))

        basis = kwargs.pop('basis')
        assert_(isinstance(basis, np.ndarray))
        assert_(basis.dtype == np.int_)

        complete = kwargs.pop('complete')
        assert_(isinstance(complete, bool))
        if complete:
            last_xk.append(xk)
            callback_complete[0] = True
        else:
            assert_(not callback_complete[0])

        # no more kwargs
        assert_(not kwargs)
    
    c = np.array([-3,-2])
    A_ub = [[2,1], [1,1], [1,0]]
    b_ub = [10,8,4]
    res = linprog(c,A_ub=A_ub,b_ub=b_ub, callback=cb)

    assert_(callback_complete[0])
    assert_allclose(last_xk[0], res.x)
