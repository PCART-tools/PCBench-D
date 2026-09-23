    def test_detrend_2D_d2_ValueError(self):
        input = self.sig_slope[np.newaxis]
        with pytest.raises(ValueError):
            mlab.detrend(input, axis=2)
