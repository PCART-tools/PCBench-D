    @cache_readonly
    def result_index(self) -> Index:
        if not self.compressed and len(self.groupings) == 1:
            return self.groupings[0].result_index.rename(self.names[0])

        codes = self.reconstructed_codes
        levels = [ping.result_index for ping in self.groupings]
        result = MultiIndex(
            levels=levels, codes=codes, verify_integrity=False, names=self.names
        )
        return result
