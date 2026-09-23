    def test_spectral_helper_raises_noverlap_eq_NFFT(self):
        # test that noverlap cannot be equal to NFFT
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, NFFT=10, noverlap=10)
