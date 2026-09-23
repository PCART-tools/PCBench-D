    def test_detrend_detrend_linear_1d_slope_off_axis1(self):
        arri = [self.sig_off,
                self.sig_slope,
                self.sig_slope + self.sig_off]
        arrt = [self.sig_zeros,
                self.sig_zeros,
                self.sig_zeros]
        input = np.vstack(arri)
        targ = np.vstack(arrt)
        res = mlab.detrend(input, key=mlab.detrend_linear, axis=1)
        assert_allclose(res, targ, atol=self.atol)
