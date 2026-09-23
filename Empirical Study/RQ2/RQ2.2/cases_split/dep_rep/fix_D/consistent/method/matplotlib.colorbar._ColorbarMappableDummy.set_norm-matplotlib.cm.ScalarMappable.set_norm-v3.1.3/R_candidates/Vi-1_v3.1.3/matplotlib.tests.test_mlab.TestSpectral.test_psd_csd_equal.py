    def test_psd_csd_equal(self):
        freqs = self.freqs_density
        Pxx, freqsxx = mlab.psd(x=self.y,
                                NFFT=self.NFFT_density,
                                Fs=self.Fs,
                                noverlap=self.nover_density,
                                pad_to=self.pad_to_density,
                                sides=self.sides)
        Pxy, freqsxy = mlab.csd(x=self.y, y=self.y,
                                NFFT=self.NFFT_density,
                                Fs=self.Fs,
                                noverlap=self.nover_density,
                                pad_to=self.pad_to_density,
                                sides=self.sides)
        assert_array_almost_equal_nulp(Pxx, Pxy)
        assert_array_equal(freqsxx, freqsxy)
