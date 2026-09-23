    def test_demean_1D_base_slope_off(self):
        input = self.sig_base + self.sig_slope + self.sig_off
        targ = self.sig_base + self.sig_slope_mean
        with pytest.warns(MatplotlibDeprecationWarning):
            res = mlab.demean(input)
        assert_allclose(res, targ, atol=1e-08)
