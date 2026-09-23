    def test_detrend_detrend_mean_2D_axis0(self):
        arri = [self.sig_base,
                self.sig_base + self.sig_off,
                self.sig_base + self.sig_slope,
                self.sig_base + self.sig_off + self.sig_slope]
        arrt = [self.sig_base,
                self.sig_base,
                self.sig_base + self.sig_slope_mean,
                self.sig_base + self.sig_slope_mean]
        input = np.vstack(arri).T
        targ = np.vstack(arrt).T
        res = mlab.detrend(input, key=mlab.detrend_mean, axis=0)
        assert_allclose(res, targ,
                        atol=1e-08)
