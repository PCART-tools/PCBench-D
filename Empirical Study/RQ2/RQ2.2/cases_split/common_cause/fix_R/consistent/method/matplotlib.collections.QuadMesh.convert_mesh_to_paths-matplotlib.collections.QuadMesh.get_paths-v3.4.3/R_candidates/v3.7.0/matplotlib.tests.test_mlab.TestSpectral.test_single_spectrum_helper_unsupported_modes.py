    @pytest.mark.parametrize('mode', ['default', 'psd'])
    def test_single_spectrum_helper_unsupported_modes(self, mode):
        with pytest.raises(ValueError):
            mlab._single_spectrum_helper(x=self.y, mode=mode)
