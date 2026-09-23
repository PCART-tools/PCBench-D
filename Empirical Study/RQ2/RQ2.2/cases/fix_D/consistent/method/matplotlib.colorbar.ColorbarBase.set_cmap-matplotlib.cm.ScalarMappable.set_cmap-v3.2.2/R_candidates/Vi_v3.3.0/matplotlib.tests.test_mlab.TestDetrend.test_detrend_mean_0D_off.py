    def test_detrend_mean_0D_off(self):
        input = 5.5
        targ = 0.
        res = mlab.detrend_mean(input)
        assert_almost_equal(res, targ)
