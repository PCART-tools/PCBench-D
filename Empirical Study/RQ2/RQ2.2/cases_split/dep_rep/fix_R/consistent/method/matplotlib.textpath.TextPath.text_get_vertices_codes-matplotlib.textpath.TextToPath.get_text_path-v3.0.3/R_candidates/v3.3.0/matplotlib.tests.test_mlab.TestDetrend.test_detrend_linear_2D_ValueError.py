    def test_detrend_linear_2D_ValueError(self):
        input = self.sig_slope[np.newaxis]
        with pytest.raises(ValueError):
            mlab.detrend_linear(input)
