    def __init__(self, comp_ids, ngroups, labels, levels):
        self.levels = levels
        self.labels = labels
        self.comp_ids = comp_ids.astype(np.int64)

        self.k = len(labels)
        self.tables = [_hash.Int64HashTable(ngroups) for _ in range(self.k)]

        self._populate_tables()
