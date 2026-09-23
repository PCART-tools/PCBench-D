    def test_angle_spectrum(self):
        freqs = self.freqs_spectrum
        spec, fsp = mlab.angle_spectrum(x=self.y,
                                        Fs=self.Fs,
                                        sides=self.sides,
                                        pad_to=self.pad_to_spectrum)
        assert_allclose(fsp, freqs, atol=1e-06)
        assert spec.shape == freqs.shape
