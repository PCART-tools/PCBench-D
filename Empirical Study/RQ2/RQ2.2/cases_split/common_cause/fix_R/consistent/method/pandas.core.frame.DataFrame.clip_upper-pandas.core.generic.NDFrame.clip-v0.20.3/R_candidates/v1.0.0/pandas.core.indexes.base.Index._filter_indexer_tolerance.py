    def _filter_indexer_tolerance(self, target, indexer, tolerance):
        distance = abs(self.values[indexer] - target)
        indexer = np.where(distance <= tolerance, indexer, -1)
        return indexer
