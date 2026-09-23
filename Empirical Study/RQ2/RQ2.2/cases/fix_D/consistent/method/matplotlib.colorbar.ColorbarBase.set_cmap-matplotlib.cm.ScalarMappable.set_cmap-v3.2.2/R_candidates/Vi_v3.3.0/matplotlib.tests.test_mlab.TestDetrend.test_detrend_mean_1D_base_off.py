    def test_detrend_mean_1D_base_off(self):
        input = self.sig_base + self.sig_off
        targ = self.sig_base
        res = mlab.detrend_mean(input)
        assert_allclose(res, targ, atol=self.atol)
