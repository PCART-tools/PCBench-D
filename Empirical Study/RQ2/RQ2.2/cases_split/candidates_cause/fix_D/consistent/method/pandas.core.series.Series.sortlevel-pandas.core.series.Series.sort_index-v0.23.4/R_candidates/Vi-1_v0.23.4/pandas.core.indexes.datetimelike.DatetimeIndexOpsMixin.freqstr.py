    @property
    def freqstr(self):
        """
        Return the frequency object as a string if it is set, otherwise None
        """
        if self.freq is None:
            return None
        return self.freq.freqstr
