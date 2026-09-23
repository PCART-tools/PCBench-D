    @Appender(_round_doc % "ceil")
    def ceil(self, freq):
        return self._round(freq, np.ceil)
