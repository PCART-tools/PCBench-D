    @final
    def _get_splitter(self, data: NDFrame, axis: int = 0) -> DataSplitter:
        """
        Returns
        -------
        Generator yielding subsetted objects
        """
        ids, _, ngroups = self.group_info
        return get_splitter(data, ids, ngroups, axis=axis)
