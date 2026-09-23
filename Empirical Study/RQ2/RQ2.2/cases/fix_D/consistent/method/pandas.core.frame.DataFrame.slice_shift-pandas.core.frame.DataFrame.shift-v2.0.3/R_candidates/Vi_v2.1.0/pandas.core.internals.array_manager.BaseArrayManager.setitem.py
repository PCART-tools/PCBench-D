    def setitem(self, indexer, value) -> Self:
        return self.apply_with_block("setitem", indexer=indexer, value=value)
