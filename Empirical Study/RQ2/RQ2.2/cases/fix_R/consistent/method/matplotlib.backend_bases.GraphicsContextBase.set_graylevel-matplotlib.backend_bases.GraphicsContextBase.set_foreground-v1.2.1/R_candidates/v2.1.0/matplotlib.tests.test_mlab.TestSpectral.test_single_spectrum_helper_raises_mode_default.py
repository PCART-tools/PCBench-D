    def test_single_spectrum_helper_raises_mode_default(self):
        # test that mode 'default' cannot be used with _single_spectrum_helper
        with pytest.raises(ValueError):
            mlab._single_spectrum_helper(x=self.y, mode='default')
