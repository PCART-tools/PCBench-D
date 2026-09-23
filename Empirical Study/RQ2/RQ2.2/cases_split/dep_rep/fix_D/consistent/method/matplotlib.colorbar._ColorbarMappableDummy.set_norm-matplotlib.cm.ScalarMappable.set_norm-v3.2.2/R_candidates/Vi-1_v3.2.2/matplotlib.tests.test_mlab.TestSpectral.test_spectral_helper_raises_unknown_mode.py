    def test_spectral_helper_raises_unknown_mode(self):
        # test that unknown value for mode cannot be used
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, mode='spam')
