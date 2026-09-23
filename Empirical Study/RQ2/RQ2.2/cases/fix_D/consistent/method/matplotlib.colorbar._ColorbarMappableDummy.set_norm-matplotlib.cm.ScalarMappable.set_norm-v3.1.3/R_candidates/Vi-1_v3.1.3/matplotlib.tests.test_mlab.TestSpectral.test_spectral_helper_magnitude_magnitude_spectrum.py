    def test_spectral_helper_magnitude_magnitude_spectrum(self):
        freqs = self.freqs_spectrum
        spec, fsp, t = mlab._spectral_helper(x=self.y, y=self.y,
                                             NFFT=self.NFFT_spectrum,
                                             Fs=self.Fs,
                                             noverlap=self.nover_spectrum,
                                             pad_to=self.pad_to_spectrum,
                                             sides=self.sides,
                                             mode='magnitude')

        assert_allclose(fsp, freqs, atol=1e-06)
        assert_allclose(t, self.t_spectrum, atol=1e-06)

        assert spec.shape[0] == freqs.shape[0]
        assert spec.shape[1] == 1
