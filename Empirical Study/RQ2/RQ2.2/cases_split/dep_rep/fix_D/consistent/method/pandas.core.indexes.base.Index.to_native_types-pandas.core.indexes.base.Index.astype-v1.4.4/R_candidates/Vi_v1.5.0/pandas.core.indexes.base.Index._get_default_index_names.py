    def _get_default_index_names(
        self, names: Hashable | Sequence[Hashable] | None = None, default=None
    ) -> list[Hashable]:
        """
        Get names of index.

        Parameters
        ----------
        names : int, str or 1-dimensional list, default None
            Index names to set.
        default : str
            Default name of index.

        Raises
        ------
        TypeError
            if names not str or list-like
        """
        from pandas.core.indexes.multi import MultiIndex

        if names is not None:
            if isinstance(names, str) or isinstance(names, int):
                names = [names]

        if not isinstance(names, list) and names is not None:
            raise ValueError("Index names must be str or 1-dimensional list")

        if not names:
            if isinstance(self, MultiIndex):
                names = com.fill_missing_names(self.names)
            else:
                names = [default] if self.name is None else [self.name]

        return names
