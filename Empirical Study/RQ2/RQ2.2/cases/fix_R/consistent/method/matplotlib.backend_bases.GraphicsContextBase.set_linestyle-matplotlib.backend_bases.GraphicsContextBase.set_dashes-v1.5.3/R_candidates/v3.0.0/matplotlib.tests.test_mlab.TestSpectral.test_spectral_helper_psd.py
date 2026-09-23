    def test_spectral_helper_psd(self):
        freqs = self.freqs_density
        spec, fsp, t = mlab._spectral_helper(x=self.y, y=self.y,
                                             NFFT=self.NFFT_density,
                                             Fs=self.Fs,
                                             noverlap=self.nover_density,
                                             pad_to=self.pad_to_density,
                                             sides=self.sides,
                                             mode='psd')

        assert_allclose(fsp, freqs, atol=1e-06)
        assert_allclose(t, self.t_density, atol=1e-06)

        assert spec.shape[0] == freqs.shape[0]
        assert spec.shape[1] == self.t_specgram.shape[0]
