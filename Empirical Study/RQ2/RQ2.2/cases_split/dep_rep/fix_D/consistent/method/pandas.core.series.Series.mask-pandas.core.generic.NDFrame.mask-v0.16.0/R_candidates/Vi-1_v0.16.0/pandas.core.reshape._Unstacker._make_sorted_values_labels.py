    def _make_sorted_values_labels(self):
        v = self.level

        labs = list(self.index.labels)
        levs = list(self.index.levels)
        to_sort = labs[:v] + labs[v + 1:] + [labs[v]]
        sizes = [len(x) for x in levs[:v] + levs[v + 1:] + [levs[v]]]

        comp_index, obs_ids = get_compressed_ids(to_sort, sizes)
        ngroups = len(obs_ids)

        indexer = algos.groupsort_indexer(comp_index, ngroups)[0]
        indexer = _ensure_platform_int(indexer)

        self.sorted_values = com.take_nd(self.values, indexer, axis=0)
        self.sorted_labels = [l.take(indexer) for l in to_sort]
