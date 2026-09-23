    def test_spectral_helper_raises_winlen_ne_NFFT(self):
        # test that the window length cannot be different from NFFT
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, y=self.y, NFFT=10,
                                  window=np.ones(9))
