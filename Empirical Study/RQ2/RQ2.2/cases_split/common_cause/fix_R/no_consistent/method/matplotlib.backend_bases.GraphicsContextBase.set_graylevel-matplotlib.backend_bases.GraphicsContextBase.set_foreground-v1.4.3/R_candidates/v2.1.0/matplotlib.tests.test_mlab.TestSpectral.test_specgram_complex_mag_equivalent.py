    def test_specgram_complex_mag_equivalent(self):
        freqs = self.freqs_specgram
        specc, freqspecc, tc = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='complex')
        specm, freqspecm, tm = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='magnitude')

        assert_array_equal(freqspecc, freqspecm)
        assert_array_equal(tc, tm)
        assert_allclose(np.abs(specc), specm, atol=1e-06)
