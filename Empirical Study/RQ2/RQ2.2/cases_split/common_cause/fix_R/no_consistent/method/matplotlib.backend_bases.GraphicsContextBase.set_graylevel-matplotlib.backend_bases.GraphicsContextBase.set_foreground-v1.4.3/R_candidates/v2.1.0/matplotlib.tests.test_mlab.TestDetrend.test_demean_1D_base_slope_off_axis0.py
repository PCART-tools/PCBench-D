    def test_demean_1D_base_slope_off_axis0(self):
        input = self.sig_base + self.sig_slope + self.sig_off
        targ = self.sig_base + self.sig_slope_mean
        res = mlab.demean(input, axis=0)
        assert_allclose(res, targ, atol=1e-08)
