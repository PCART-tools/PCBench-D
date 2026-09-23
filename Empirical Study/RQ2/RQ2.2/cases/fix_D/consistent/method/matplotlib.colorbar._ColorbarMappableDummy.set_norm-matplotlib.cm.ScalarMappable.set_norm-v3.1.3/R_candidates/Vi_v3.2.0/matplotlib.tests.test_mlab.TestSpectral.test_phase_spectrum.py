    def test_phase_spectrum(self):
        freqs = self.freqs_spectrum
        spec, fsp = mlab.phase_spectrum(x=self.y,
                                        Fs=self.Fs,
                                        sides=self.sides,
                                        pad_to=self.pad_to_spectrum)
        assert_allclose(fsp, freqs, atol=1e-06)
        assert spec.shape == freqs.shape
