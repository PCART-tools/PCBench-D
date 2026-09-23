    @Appender(_round_doc % "round")
    def round(self, freq, *args, **kwargs):
        return self._round(freq, np.round)
