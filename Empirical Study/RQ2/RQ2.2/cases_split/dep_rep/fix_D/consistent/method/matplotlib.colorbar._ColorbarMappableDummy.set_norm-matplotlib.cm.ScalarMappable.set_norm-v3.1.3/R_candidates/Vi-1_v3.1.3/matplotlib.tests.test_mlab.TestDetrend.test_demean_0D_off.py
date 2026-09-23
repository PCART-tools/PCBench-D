    def test_demean_0D_off(self):
        input = 5.5
        targ = 0.
        with pytest.warns(MatplotlibDeprecationWarning):
            res = mlab.demean(input, axis=None)
        assert_almost_equal(res, targ)
