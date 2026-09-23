    def test_spectral_helper_raises_noverlap_gt_NFFT(self):
        # test that noverlap cannot be larger than NFFT
        with pytest.raises(ValueError):
            mlab._spectral_helper(x=self.y, y=self.y, NFFT=10, noverlap=20)
