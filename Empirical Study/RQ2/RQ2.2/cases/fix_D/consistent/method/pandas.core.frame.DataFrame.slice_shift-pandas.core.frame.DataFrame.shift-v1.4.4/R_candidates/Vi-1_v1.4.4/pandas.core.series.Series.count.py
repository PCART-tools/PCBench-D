    def count(self, level=None):
        """
        Return number of non-NA/null observations in the Series.

        Parameters
        ----------
        level : int or level name, default None
            If the axis is a MultiIndex (hierarchical), count along a
            particular level, collapsing into a smaller Series.

        Returns
        -------
        int or Series (if level specified)
            Number of non-null values in the Series.

        See Also
        --------
        DataFrame.count : Count non-NA cells for each column or row.

        Examples
        --------
        >>> s = pd.Series([0.0, 1.0, np.nan])
        >>> s.count()
        2
        """
        if level is None:
            return notna(self._values).sum().astype("int64")
        else:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. ser.count(level=1) should use ser.groupby(level=1).count().",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            if not isinstance(self.index, MultiIndex):
                raise ValueError("Series.count level is only valid with a MultiIndex")

        index = self.index
        assert isinstance(index, MultiIndex)  # for mypy

        if isinstance(level, str):
            level = index._get_level_number(level)

        lev = index.levels[level]
        level_codes = np.array(index.codes[level], subok=False, copy=True)

        mask = level_codes == -1
        if mask.any():
            level_codes[mask] = cnt = len(lev)
            lev = lev.insert(cnt, lev._na_value)

        obs = level_codes[notna(self._values)]
        # Argument "minlength" to "bincount" has incompatible type "Optional[int]";
        # expected "SupportsIndex"  [arg-type]
        out = np.bincount(obs, minlength=len(lev) or None)  # type: ignore[arg-type]
        return self._constructor(out, index=lev, dtype="int64").__finalize__(
            self, method="count"
        )
