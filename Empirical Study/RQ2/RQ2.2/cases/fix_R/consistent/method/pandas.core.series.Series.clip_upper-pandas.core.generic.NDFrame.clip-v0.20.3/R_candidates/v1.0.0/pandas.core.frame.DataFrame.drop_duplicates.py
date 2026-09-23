    def drop_duplicates(
        self,
        subset: Optional[Union[Hashable, Sequence[Hashable]]] = None,
        keep: Union[str, bool] = "first",
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> Optional["DataFrame"]:
        """
        Return DataFrame with duplicate rows removed.

        Considering certain columns is optional. Indexes, including time indexes
        are ignored.

        Parameters
        ----------
        subset : column label or sequence of labels, optional
            Only consider certain columns for identifying duplicates, by
            default use all of the columns.
        keep : {'first', 'last', False}, default 'first'
            Determines which duplicates (if any) to keep.
            - ``first`` : Drop duplicates except for the first occurrence.
            - ``last`` : Drop duplicates except for the last occurrence.
            - False : Drop all duplicates.
        inplace : bool, default False
            Whether to drop duplicates in place or to return a copy.
        ignore_index : bool, default False
            If True, the resulting axis will be labeled 0, 1, …, n - 1.

            .. versionadded:: 1.0.0

        Returns
        -------
        DataFrame
            DataFrame with duplicates removed or None if ``inplace=True``.
        """
        if self.empty:
            return self.copy()

        inplace = validate_bool_kwarg(inplace, "inplace")
        duplicated = self.duplicated(subset, keep=keep)

        if inplace:
            (inds,) = (-duplicated)._ndarray_values.nonzero()
            new_data = self._data.take(inds)

            if ignore_index:
                new_data.axes[1] = ibase.default_index(len(inds))
            self._update_inplace(new_data)
        else:
            result = self[-duplicated]

            if ignore_index:
                result.index = ibase.default_index(len(result))
            return result

        return None
