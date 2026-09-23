    def test_demean_2D_default(self):
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
        res = mlab.demean(input)
        assert_allclose(res, targ,
                        atol=1e-08)
