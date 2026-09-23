    @cache_readonly
    def result_index(self):
        if len(self.binlabels) != 0 and isnull(self.binlabels[0]):
            return self.binlabels[1:]

        return self.binlabels
