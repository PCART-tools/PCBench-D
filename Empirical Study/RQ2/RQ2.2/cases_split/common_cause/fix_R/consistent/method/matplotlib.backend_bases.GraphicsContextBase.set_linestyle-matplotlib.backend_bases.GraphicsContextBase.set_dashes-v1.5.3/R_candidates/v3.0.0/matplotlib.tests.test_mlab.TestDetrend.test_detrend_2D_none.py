    def test_detrend_2D_none(self):
        arri = [self.sig_off,
                self.sig_base + self.sig_off]
        arrt = [self.sig_zeros,
                self.sig_base]
        input = np.vstack(arri)
        targ = np.vstack(arrt)
        res = mlab.detrend(input, axis=None)
        assert_allclose(res, targ, atol=1e-08)
