    @final
    def _get_splitter(self, data: NDFrame, axis: int = 0) -> DataSplitter:
        """
        Returns
        -------
        Generator yielding subsetted objects

        __finalize__ has not been called for the subsetted objects returned.
        """
        ids, _, ngroups = self.group_info
        return get_splitter(data, ids, ngroups, axis=axis)
