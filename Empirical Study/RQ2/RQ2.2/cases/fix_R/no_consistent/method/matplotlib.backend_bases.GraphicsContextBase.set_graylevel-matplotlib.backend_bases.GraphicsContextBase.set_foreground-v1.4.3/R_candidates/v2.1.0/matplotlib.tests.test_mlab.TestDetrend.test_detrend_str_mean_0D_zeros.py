    def test_detrend_str_mean_0D_zeros(self):
        input = 0.
        targ = 0.
        res = mlab.detrend(input, key='mean')
        assert_almost_equal(res, targ)
