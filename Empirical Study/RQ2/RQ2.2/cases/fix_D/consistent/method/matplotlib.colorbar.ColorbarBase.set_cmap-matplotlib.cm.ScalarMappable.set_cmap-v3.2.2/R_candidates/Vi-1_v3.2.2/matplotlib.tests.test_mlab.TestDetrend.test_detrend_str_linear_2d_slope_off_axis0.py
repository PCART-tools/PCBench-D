    def test_detrend_str_linear_2d_slope_off_axis0(self):
        arri = [self.sig_off,
                self.sig_slope,
                self.sig_slope + self.sig_off]
        arrt = [self.sig_zeros,
                self.sig_zeros,
                self.sig_zeros]
        input = np.vstack(arri).T
        targ = np.vstack(arrt).T
        res = mlab.detrend(input, key='linear', axis=0)
        assert_allclose(res, targ, atol=self.atol)
