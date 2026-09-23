    def test_psd(self):
        freqs = self.freqs_density
        spec, fsp = mlab.psd(x=self.y,
                             NFFT=self.NFFT_density,
                             Fs=self.Fs,
                             noverlap=self.nover_density,
                             pad_to=self.pad_to_density,
                             sides=self.sides)
        assert spec.shape == freqs.shape
        self.check_freqs(spec, freqs, fsp, self.fstims)
