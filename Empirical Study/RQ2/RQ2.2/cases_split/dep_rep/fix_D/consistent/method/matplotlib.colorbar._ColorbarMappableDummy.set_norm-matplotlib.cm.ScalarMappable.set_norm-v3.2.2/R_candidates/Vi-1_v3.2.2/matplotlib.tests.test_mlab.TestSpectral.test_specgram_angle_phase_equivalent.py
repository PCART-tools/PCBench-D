    def test_specgram_angle_phase_equivalent(self):
        speca, freqspeca, ta = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='angle')
        specp, freqspecp, tp = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='phase')

        assert_array_equal(freqspeca, freqspecp)
        assert_array_equal(ta, tp)
        assert_allclose(np.unwrap(speca, axis=0), specp,
                        atol=1e-06)
