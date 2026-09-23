    def test_detrend_mean_1D_zeros(self):
        input = self.sig_zeros
        targ = self.sig_zeros
        res = mlab.detrend_mean(input)
        assert_allclose(res, targ, atol=self.atol)
