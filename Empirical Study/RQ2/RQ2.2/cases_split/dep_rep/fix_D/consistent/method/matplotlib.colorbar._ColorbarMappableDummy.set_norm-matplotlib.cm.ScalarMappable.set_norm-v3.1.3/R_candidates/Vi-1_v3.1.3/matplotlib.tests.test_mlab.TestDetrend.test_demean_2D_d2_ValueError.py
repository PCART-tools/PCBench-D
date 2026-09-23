    def test_demean_2D_d2_ValueError(self):
        input = self.sig_slope[np.newaxis]
        with pytest.raises(ValueError):
            mlab.demean(input, axis=2)
