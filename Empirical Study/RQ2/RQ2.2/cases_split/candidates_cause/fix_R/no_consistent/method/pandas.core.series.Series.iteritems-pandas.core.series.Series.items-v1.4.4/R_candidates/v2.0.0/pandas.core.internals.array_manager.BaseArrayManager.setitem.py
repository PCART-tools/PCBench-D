    def setitem(self: T, indexer, value) -> T:
        return self.apply_with_block("setitem", indexer=indexer, value=value)
