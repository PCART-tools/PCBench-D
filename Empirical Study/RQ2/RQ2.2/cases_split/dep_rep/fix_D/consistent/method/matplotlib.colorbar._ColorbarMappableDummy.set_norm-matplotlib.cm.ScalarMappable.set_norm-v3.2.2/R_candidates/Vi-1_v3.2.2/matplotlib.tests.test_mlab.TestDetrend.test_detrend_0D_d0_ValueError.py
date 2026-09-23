    def test_detrend_0D_d0_ValueError(self):
        input = 5.5
        with pytest.raises(ValueError):
            mlab.detrend(input, axis=0)
