    @final
    @cache_readonly
    def codes_info(self) -> npt.NDArray[np.intp]:
        # return the codes of items in original grouped axis
        ids, _, _ = self.group_info
        if self.indexer is not None:
            sorter = np.lexsort((ids, self.indexer))
            ids = ids[sorter]
            ids = ensure_platform_int(ids)
            # TODO: if numpy annotates np.lexsort, this ensure_platform_int
            #  may become unnecessary
        return ids
