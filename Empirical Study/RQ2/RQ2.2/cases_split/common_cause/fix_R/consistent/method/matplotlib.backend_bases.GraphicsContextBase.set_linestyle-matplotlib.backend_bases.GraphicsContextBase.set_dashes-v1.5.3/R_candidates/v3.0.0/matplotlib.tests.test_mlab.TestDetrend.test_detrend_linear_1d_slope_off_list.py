    def test_detrend_linear_1d_slope_off_list(self):
        input = self.sig_slope + self.sig_off
        targ = self.sig_zeros
        res = mlab.detrend_linear(input.tolist())
        assert_allclose(res, targ, atol=self.atol)
