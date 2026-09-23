    def __unicode__(self):
        return "period[{freq}]".format(freq=self.freq.freqstr)
