    def test_detrend_str_linear_1d_slope_off(self):
        input = self.sig_slope + self.sig_off
        targ = self.sig_zeros
        res = mlab.detrend(input, key='linear')
        assert_allclose(res, targ, atol=self.atol)
