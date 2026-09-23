    @final
    def _get_splitter(self, data: NDFrame, axis: AxisInt = 0) -> DataSplitter:
        """
        Returns
        -------
        Generator yielding subsetted objects
        """
        ids, _, ngroups = self.group_info
        return _get_splitter(
            data,
            ids,
            ngroups,
            sorted_ids=self._sorted_ids,
            sort_idx=self._sort_idx,
            axis=axis,
        )
