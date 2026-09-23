    @Appender(_round_doc % "floor")
    def floor(self, freq):
        return self._round(freq, np.floor)
