    def test_detrend_mean_1D_d1_ValueError(self):
        input = self.sig_slope
        with pytest.raises(ValueError):
            mlab.detrend_mean(input, axis=1)
