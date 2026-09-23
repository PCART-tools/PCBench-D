    def test_detrend_str_linear_2d_slope_off_axis0(self):
        arri = [self.sig_off,
                self.sig_slope,
                self.sig_slope + self.sig_off]
        arrt = [self.sig_zeros,
                self.sig_zeros,
                self.sig_zeros]
        input = np.vstack(arri)
        targ = np.vstack(arrt)
        res = mlab.detrend(input, key='linear', axis=1)
        assert_allclose(res, targ, atol=self.atol)
