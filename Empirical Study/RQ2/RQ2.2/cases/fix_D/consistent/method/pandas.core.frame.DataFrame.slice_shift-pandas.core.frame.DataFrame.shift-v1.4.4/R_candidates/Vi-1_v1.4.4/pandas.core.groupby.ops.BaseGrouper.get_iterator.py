    def get_iterator(
        self, data: NDFrameT, axis: int = 0
    ) -> Iterator[tuple[Hashable, NDFrameT]]:
        """
        Groupby iterator

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group
        """
        splitter = self._get_splitter(data, axis=axis)
        keys = self.group_keys_seq
        for key, group in zip(keys, splitter):
            yield key, group.__finalize__(data, method="groupby")
