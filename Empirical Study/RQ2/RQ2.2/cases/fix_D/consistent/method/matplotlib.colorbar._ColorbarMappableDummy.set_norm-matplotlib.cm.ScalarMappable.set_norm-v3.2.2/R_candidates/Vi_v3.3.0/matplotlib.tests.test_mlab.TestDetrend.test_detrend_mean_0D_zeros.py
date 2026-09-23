    def test_detrend_mean_0D_zeros(self):
        input = 0.
        targ = 0.
        res = mlab.detrend_mean(input)
        assert_almost_equal(res, targ)
