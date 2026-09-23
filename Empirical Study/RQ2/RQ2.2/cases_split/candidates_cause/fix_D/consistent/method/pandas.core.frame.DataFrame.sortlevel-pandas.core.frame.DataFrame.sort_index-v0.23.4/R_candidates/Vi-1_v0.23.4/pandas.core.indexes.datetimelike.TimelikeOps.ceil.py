    @Appender((_round_doc + _ceil_example).format(op="ceil"))
    def ceil(self, freq):
        return self._round(freq, np.ceil)
