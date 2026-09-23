    def _make_sorted_values_labels(self):
        v = self.level

        codes = list(self.index.codes)
        levs = list(self.index.levels)
        to_sort = codes[:v] + codes[v + 1 :] + [codes[v]]
        sizes = [len(x) for x in levs[:v] + levs[v + 1 :] + [levs[v]]]

        comp_index, obs_ids = get_compressed_ids(to_sort, sizes)
        ngroups = len(obs_ids)

        indexer = libalgos.groupsort_indexer(comp_index, ngroups)[0]
        indexer = ensure_platform_int(indexer)

        self.sorted_values = algos.take_nd(self.values, indexer, axis=0)
        self.sorted_labels = [l.take(indexer) for l in to_sort]
