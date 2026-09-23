    def setitem(self: T, indexer, value) -> T:
        """
        Set values with indexer.

        For SingleBlockManager, this backs s[indexer] = value
        """
        return self.apply("setitem", indexer=indexer, value=value)
