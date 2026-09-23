    @cache_readonly
    def codes_info(self) -> np.ndarray:
        # return the codes of items in original grouped axis
        codes, _, _ = self.group_info
        if self.indexer is not None:
            sorter = np.lexsort((codes, self.indexer))
            codes = codes[sorter]
        return codes
