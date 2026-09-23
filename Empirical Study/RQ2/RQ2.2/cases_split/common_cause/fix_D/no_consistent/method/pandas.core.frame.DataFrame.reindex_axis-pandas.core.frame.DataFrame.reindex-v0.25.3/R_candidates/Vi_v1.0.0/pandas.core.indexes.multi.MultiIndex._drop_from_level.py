    def _drop_from_level(self, codes, level, errors="raise"):
        codes = com.index_labels_to_array(codes)
        i = self._get_level_number(level)
        index = self.levels[i]
        values = index.get_indexer(codes)

        mask = ~algos.isin(self.codes[i], values)
        if mask.all() and errors != "ignore":
            raise KeyError(f"labels {codes} not found in level")

        return self[mask]
