    @cache_readonly
    def indices(self):
        indices = collections.defaultdict(list)

        i = 0
        for label, bin in zip(self.binlabels, self.bins):
            if i < bin:
                if label is not tslib.NaT:
                    indices[label] = list(range(i, bin))
                i = bin
        return indices
