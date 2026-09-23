    def test_detrend_mean_1D_base(self):
        input = self.sig_base
        targ = self.sig_base
        res = mlab.detrend_mean(input)
        assert_allclose(res, targ, atol=self.atol)
