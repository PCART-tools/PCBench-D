    def _drop_from_level(self, labels, level):
        labels = com._index_labels_to_array(labels)
        i = self._get_level_number(level)
        index = self.levels[i]
        values = index.get_indexer(labels)

        mask = ~algos.isin(self.labels[i], values)

        return self[mask]
