    def test_detrend_1D_d1_ValueError(self):
        input = self.sig_slope
        with pytest.raises(ValueError):
            mlab.detrend(input, axis=1)
