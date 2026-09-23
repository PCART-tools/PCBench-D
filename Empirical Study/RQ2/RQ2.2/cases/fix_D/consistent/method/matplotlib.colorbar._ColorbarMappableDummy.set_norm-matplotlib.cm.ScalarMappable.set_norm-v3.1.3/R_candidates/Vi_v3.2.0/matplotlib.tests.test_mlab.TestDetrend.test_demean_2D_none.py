    def test_demean_2D_none(self):
        arri = [self.sig_off,
                self.sig_base + self.sig_off]
        arrt = [self.sig_zeros,
                self.sig_base]
        input = np.vstack(arri)
        targ = np.vstack(arrt)
        with pytest.warns(MatplotlibDeprecationWarning):
            res = mlab.demean(input, axis=None)
        assert_allclose(res, targ,
                        atol=1e-08)
