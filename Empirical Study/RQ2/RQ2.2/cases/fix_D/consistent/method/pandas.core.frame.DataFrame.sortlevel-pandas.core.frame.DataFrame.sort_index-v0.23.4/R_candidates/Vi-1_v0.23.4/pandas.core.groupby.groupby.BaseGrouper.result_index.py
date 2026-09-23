    @cache_readonly
    def result_index(self):
        if not self.compressed and len(self.groupings) == 1:
            return self.groupings[0].result_index.rename(self.names[0])

        labels = self.recons_labels
        levels = [ping.result_index for ping in self.groupings]
        result = MultiIndex(levels=levels,
                            labels=labels,
                            verify_integrity=False,
                            names=self.names)
        return result
