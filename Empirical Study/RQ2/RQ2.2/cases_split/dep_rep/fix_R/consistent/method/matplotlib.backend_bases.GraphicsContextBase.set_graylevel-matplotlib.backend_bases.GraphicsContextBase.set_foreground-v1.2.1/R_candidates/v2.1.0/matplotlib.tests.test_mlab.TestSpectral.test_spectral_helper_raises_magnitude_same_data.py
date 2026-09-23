    def test_spectral_helper_raises_magnitude_same_data(self):
        # test that mode 'magnitude' cannot be used if x is not y
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, y=self.y+1, mode='magnitude')
