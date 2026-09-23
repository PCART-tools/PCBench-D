    @final
    def __iter__(self) -> Iterator[tuple[Hashable, NDFrameT]]:
        """
        Groupby iterator.

        Returns
        -------
        Generator yielding sequence of (name, subsetted object)
        for each group
        """
        keys = self.keys
        result = self.grouper.get_iterator(self._selected_obj, axis=self.axis)
        if isinstance(keys, list) and len(keys) == 1:
            # GH#42795 - when keys is a list, return tuples even when length is 1
            result = (((key,), group) for key, group in result)
        return result
