    def test_detrend_none_1D_slope(self):
        input = self.sig_slope
        targ = input
        res = mlab.detrend_none(input)
        assert_array_equal(res, targ)
