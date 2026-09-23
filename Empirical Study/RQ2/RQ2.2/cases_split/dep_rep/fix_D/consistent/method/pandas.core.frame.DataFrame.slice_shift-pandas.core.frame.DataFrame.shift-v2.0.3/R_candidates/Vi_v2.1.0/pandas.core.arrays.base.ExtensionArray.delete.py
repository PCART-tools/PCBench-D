    def delete(self, loc: PositionalIndexer) -> Self:
        indexer = np.delete(np.arange(len(self)), loc)
        return self.take(indexer)
