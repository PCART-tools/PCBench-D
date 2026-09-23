    @Appender((_round_doc + _floor_example).format(op="floor"))
    def floor(self, freq):
        return self._round(freq, np.floor)
