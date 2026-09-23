    @cache_readonly
    def result_index(self):
        if not self.compressed and len(self.groupings) == 1:
            return self.groupings[0].group_index.rename(self.names[0])

        return MultiIndex(levels=[ping.group_index for ping in self.groupings],
                          labels=self.recons_labels,
                          verify_integrity=False,
                          names=self.names)
