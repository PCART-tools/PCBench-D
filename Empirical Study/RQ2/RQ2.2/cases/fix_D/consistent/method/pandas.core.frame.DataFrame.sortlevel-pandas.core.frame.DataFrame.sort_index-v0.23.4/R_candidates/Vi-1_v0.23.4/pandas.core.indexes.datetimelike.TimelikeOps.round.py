    @Appender((_round_doc + _round_example).format(op="round"))
    def round(self, freq, *args, **kwargs):
        return self._round(freq, np.round)
