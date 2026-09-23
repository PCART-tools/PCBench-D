    def test_detrend_none(self):
        assert mlab.detrend_none(0.) == 0.
        assert mlab.detrend_none(0., axis=1) == 0.
        assert mlab.detrend(0., key="none") == 0.
        assert mlab.detrend(0., key=mlab.detrend_none) == 0.
        for sig in [
                5.5, self.sig_off, self.sig_slope, self.sig_base,
                (self.sig_base + self.sig_slope + self.sig_off).tolist(),
                np.vstack([self.sig_base,  # 2D case.
                           self.sig_base + self.sig_off,
                           self.sig_base + self.sig_slope,
                           self.sig_base + self.sig_off + self.sig_slope]),
                np.vstack([self.sig_base,  # 2D transposed case.
                           self.sig_base + self.sig_off,
                           self.sig_base + self.sig_slope,
                           self.sig_base + self.sig_off + self.sig_slope]).T,
        ]:
            if isinstance(sig, np.ndarray):
                assert_array_equal(mlab.detrend_none(sig), sig)
            else:
                assert mlab.detrend_none(sig) == sig
