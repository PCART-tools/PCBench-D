    def test_detrend_linear(self):
        # 0D.
        assert mlab.detrend_linear(0.) == 0.
        assert mlab.detrend_linear(5.5) == 0.
        assert mlab.detrend(5.5, key="linear") == 0.
        assert mlab.detrend(5.5, key=mlab.detrend_linear) == 0.
        for sig in [  # 1D.
                self.sig_off,
                self.sig_slope,
                self.sig_slope + self.sig_off,
        ]:
            self.allclose(mlab.detrend_linear(sig), self.sig_zeros)
