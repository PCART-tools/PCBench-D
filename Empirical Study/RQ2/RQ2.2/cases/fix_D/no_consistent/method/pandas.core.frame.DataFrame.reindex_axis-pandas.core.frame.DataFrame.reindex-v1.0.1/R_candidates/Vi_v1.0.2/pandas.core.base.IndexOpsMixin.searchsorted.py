    @Substitution(klass="Index")
    @Appender(_shared_docs["searchsorted"])
    def searchsorted(self, value, side="left", sorter=None):
        return algorithms.searchsorted(self._values, value, side=side, sorter=sorter)
