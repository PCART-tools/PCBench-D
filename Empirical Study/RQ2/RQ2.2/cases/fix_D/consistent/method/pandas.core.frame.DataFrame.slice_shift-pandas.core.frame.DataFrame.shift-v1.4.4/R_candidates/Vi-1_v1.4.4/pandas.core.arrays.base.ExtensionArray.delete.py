    def delete(self: ExtensionArrayT, loc: PositionalIndexer) -> ExtensionArrayT:
        indexer = np.delete(np.arange(len(self)), loc)
        return self.take(indexer)
