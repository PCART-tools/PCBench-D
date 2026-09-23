    def test_demean_1D_d1_ValueError(self):
        input = self.sig_slope
        with pytest.raises(ValueError), \
             pytest.warns(MatplotlibDeprecationWarning):
            mlab.demean(input, axis=1)
