    def test_specgram_auto_psd_equal(self):
        '''test that mlab.specgram without mode and with mode 'default' and
        'psd' are all the same'''
        speca, freqspeca, ta = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides)
        specc, freqspecc, tc = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='psd')
        assert_array_equal(speca, specc)
        assert_array_equal(freqspeca, freqspecc)
        assert_array_equal(ta, tc)
