    def test_detrend_bad_key_var_ValueError(self):
        input = self.sig_slope[np.newaxis]
        with pytest.raises(ValueError):
            mlab.detrend(input, key=5)
