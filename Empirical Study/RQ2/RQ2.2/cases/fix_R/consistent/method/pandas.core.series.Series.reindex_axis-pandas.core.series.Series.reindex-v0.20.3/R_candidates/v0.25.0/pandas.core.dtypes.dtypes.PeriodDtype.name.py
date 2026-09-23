    @property
    def name(self):
        return "period[{freq}]".format(freq=self.freq.freqstr)
