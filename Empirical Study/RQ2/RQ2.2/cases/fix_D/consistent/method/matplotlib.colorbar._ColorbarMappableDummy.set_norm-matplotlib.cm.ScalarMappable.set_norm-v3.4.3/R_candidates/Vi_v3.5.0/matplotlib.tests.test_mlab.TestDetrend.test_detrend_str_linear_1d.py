    def test_detrend_str_linear_1d(self):
        input = self.sig_slope + self.sig_off
        target = self.sig_zeros
        self.allclose(mlab.detrend(input, key="linear"), target)
        self.allclose(mlab.detrend(input, key=mlab.detrend_linear), target)
        self.allclose(mlab.detrend_linear(input.tolist()), target)
