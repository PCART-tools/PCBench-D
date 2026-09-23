    def test_specgram_warn_only1seg(self):
        """Warning should be raised if len(x) <= NFFT."""
        with pytest.warns(UserWarning, match="Only one segment is calculated"):
            mlab.specgram(x=self.y, NFFT=len(self.y), Fs=self.Fs)
