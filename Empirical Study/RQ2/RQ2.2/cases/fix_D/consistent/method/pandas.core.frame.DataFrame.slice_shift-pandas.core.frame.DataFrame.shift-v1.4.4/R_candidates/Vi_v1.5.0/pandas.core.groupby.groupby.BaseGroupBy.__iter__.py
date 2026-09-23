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
        if isinstance(keys, list) and len(keys) == 1:
            warnings.warn(
                (
                    "In a future version of pandas, a length 1 "
                    "tuple will be returned when iterating over a "
                    "groupby with a grouper equal to a list of "
                    "length 1. Don't supply a list with a single grouper "
                    "to avoid this warning."
                ),
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        return self.grouper.get_iterator(self._selected_obj, axis=self.axis)
