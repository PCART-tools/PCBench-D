    def test_specgram_complex_angle_equivalent(self):
        freqs = self.freqs_specgram
        specc, freqspecc, tc = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='complex')
        speca, freqspeca, ta = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='angle')

        assert_array_equal(freqspecc, freqspeca)
        assert_array_equal(tc, ta)
        assert_allclose(np.angle(specc), speca, atol=1e-06)
