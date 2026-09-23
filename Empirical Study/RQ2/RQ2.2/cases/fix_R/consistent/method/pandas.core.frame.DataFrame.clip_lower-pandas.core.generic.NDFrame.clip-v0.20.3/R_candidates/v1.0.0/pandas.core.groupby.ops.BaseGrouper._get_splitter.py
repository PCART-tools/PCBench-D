    def _get_splitter(self, data: FrameOrSeries, axis: int = 0) -> "DataSplitter":
        comp_ids, _, ngroups = self.group_info
        return get_splitter(data, comp_ids, ngroups, axis=axis)
