    def test_magnitude_spectrum(self):
        freqs = self.freqs_spectrum
        spec, fsp = mlab.magnitude_spectrum(x=self.y,
                                            Fs=self.Fs,
                                            sides=self.sides,
                                            pad_to=self.pad_to_spectrum)
        assert spec.shape == freqs.shape
        self.check_maxfreq(spec, fsp, self.fstims)
        self.check_freqs(spec, freqs, fsp, self.fstims)
