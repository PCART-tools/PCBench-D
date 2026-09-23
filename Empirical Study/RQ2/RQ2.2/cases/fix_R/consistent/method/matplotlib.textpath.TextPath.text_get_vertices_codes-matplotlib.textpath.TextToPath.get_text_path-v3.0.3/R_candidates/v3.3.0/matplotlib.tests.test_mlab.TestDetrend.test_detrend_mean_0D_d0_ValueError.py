    def test_detrend_mean_0D_d0_ValueError(self):
        input = 5.5
        with pytest.raises(ValueError):
            mlab.detrend_mean(input, axis=0)
