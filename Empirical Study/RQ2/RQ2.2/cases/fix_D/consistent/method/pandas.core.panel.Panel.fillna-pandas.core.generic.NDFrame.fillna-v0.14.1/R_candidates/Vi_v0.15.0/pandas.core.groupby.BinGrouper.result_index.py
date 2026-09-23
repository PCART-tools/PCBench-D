    @cache_readonly
    def result_index(self):
        mask = self.binlabels.asi8 == tslib.iNaT
        return self.binlabels[~mask]
