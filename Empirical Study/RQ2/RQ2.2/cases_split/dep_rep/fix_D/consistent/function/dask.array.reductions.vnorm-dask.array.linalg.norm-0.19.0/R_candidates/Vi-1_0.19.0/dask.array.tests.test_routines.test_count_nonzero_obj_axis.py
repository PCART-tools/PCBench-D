@pytest.mark.skipif(LooseVersion(np.__version__) < '1.12.0',
                    reason="NumPy's count_nonzero doesn't yet support axis")
@pytest.mark.parametrize('axis', [None, 0, (1,), (0, 1)])
def test_count_nonzero_obj_axis(axis):
    x = np.random.randint(10, size=(15, 16)).astype(object)
    d = da.from_array(x, chunks=(4, 5))

    x_c = np.count_nonzero(x, axis)
    d_c = da.count_nonzero(d, axis)

    if d_c.shape == tuple():
        assert x_c == d_c.compute()
    else:
        #######################################################
        # Workaround oddness with Windows and object arrays.  #
        #                                                     #
        # xref: https://github.com/numpy/numpy/issues/9468    #
        #######################################################
        assert_eq(x_c.astype(np.intp), d_c)
