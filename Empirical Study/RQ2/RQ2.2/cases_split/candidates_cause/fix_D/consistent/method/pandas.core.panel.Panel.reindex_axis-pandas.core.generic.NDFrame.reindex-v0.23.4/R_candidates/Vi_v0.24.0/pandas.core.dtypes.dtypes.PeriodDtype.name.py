    @property
    def name(self):
        return str("period[{freq}]".format(freq=self.freq.freqstr))
