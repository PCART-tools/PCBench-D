    def test_spectral_helper_raises_unknown_sides(self):
        # test that unknown value for sides cannot be used
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, y=self.y, sides='eggs')
