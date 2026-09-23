    def test_specgram_auto_default_equal(self):
        '''test that mlab.specgram without mode and with mode 'default' and
        'psd' are all the same'''
        freqs = self.freqs_specgram
        speca, freqspeca, ta = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides)
        specb, freqspecb, tb = mlab.specgram(x=self.y,
                                             NFFT=self.NFFT_specgram,
                                             Fs=self.Fs,
                                             noverlap=self.nover_specgram,
                                             pad_to=self.pad_to_specgram,
                                             sides=self.sides,
                                             mode='default')
        assert_array_equal(speca, specb)
        assert_array_equal(freqspeca, freqspecb)
        assert_array_equal(ta, tb)
