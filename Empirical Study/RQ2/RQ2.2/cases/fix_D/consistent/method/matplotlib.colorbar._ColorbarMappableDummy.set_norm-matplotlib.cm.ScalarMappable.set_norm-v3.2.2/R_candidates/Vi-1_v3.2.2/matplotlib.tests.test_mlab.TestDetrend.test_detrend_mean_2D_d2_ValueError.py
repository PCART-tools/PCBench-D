    def test_detrend_mean_2D_d2_ValueError(self):
        input = self.sig_slope[np.newaxis]
        with pytest.raises(ValueError):
            mlab.detrend_mean(input, axis=2)
