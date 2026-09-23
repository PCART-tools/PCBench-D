    def test_demean_2D_axis1(self):
        arri = [self.sig_base,
                self.sig_base + self.sig_off,
                self.sig_base + self.sig_slope,
                self.sig_base + self.sig_off + self.sig_slope]
        arrt = [self.sig_base,
                self.sig_base,
                self.sig_base + self.sig_slope_mean,
                self.sig_base + self.sig_slope_mean]
        input = np.vstack(arri)
        targ = np.vstack(arrt)
        with pytest.warns(MatplotlibDeprecationWarning):
            res = mlab.demean(input, axis=1)
        assert_allclose(res, targ,
                        atol=1e-08)
