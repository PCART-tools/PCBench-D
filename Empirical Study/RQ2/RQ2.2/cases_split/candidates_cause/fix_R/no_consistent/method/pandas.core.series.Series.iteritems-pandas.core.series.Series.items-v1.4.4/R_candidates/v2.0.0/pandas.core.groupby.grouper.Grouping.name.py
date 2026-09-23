    @cache_readonly
    def name(self) -> Hashable:
        ilevel = self._ilevel
        if ilevel is not None:
            return self._index.names[ilevel]

        if isinstance(self._orig_grouper, (Index, Series)):
            return self._orig_grouper.name

        elif isinstance(self.grouping_vector, ops.BaseGrouper):
            return self.grouping_vector.result_index.name

        elif isinstance(self.grouping_vector, Index):
            return self.grouping_vector.name

        # otherwise we have ndarray or ExtensionArray -> no name
        return None
