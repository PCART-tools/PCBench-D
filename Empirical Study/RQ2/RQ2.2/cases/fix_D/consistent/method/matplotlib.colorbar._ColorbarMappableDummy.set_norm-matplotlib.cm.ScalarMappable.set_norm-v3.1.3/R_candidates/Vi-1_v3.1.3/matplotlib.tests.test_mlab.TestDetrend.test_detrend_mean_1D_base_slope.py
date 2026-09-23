    def test_detrend_mean_1D_base_slope(self):
        input = self.sig_base + self.sig_slope
        targ = self.sig_base + self.sig_slope_mean
        res = mlab.detrend_mean(input)
        assert_allclose(res, targ, atol=self.atol)
