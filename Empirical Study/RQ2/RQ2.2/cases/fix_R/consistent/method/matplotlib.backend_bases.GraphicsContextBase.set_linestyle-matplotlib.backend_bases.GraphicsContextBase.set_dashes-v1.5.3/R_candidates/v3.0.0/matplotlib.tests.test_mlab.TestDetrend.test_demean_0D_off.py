    def test_demean_0D_off(self):
        input = 5.5
        targ = 0.
        res = mlab.demean(input, axis=None)
        assert_almost_equal(res, targ)
