    def _get_level_indexer(self, key, level=0):
        level_index = self.levels[level]
        loc = level_index.get_loc(key)
        labels = self.labels[level]

        if level > 0 or self.lexsort_depth == 0:
            return labels == loc
        else:
            # sorted, so can return slice object -> view
            i = labels.searchsorted(loc, side='left')
            j = labels.searchsorted(loc, side='right')
            return slice(i, j)
