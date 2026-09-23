    def test_specgram_phase(self):
        freqs = self.freqs_specgram
        spec, fsp, t = mlab.specgram(x=self.y,
                                     NFFT=self.NFFT_specgram,
                                     Fs=self.Fs,
                                     noverlap=self.nover_specgram,
                                     pad_to=self.pad_to_specgram,
                                     sides=self.sides,
                                     mode='phase')
        specm = np.mean(spec, axis=1)

        assert_allclose(fsp, freqs, atol=1e-06)
        assert_allclose(t, self.t_specgram, atol=1e-06)

        assert spec.shape[0] == freqs.shape[0]
        assert spec.shape[1] == self.t_specgram.shape[0]
