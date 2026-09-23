    def test_specgram_warn_only1seg(self):
        """Warning should be raised if len(x) <= NFFT. """
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", category=UserWarning)
            mlab.specgram(x=self.y, NFFT=len(self.y), Fs=self.Fs)
        assert len(w) == 1
        assert issubclass(w[0].category, UserWarning)
        assert str(w[0].message).startswith("Only one segment is calculated")
