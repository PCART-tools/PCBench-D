    def test_specgram_complex_phase_equivalent(self):
        specc, freqspecc, tc = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='complex')
        specp, freqspecp, tp = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='phase')

        assert_array_equal(freqspecc, freqspecp)
        assert_array_equal(tc, tp)
        assert_allclose(np.unwrap(np.angle(specc), axis=0), specp,
                        atol=1e-06)
