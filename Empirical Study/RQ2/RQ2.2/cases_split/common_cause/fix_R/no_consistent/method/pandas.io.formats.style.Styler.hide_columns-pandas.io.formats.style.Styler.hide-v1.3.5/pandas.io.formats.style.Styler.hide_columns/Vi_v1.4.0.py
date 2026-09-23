    def hide_columns(
        self,
        subset: Subset | None = None,
        level: Level | list[Level] | None = None,
        names: bool = False,
    ) -> Styler:
        """
        Hide the column headers or specific keys in the columns from rendering.

        This method has dual functionality:

          - if ``subset`` is ``None`` then the entire column headers row, or
            specific levels, will be hidden whilst the data-values remain visible.
          - if a ``subset`` is given then those specific columns, including the
            data-values will be hidden, whilst the column headers row remains visible.

        .. versionchanged:: 1.3.0

        ..deprecated:: 1.4.0
          This method should be replaced by ``hide(axis="columns", **kwargs)``

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 1d input or single key along the columns axis within
            `DataFrame.loc[:, <subset>]`, to limit ``data`` to *before* applying
            the function.
        level : int, str, list
            The level(s) to hide in a MultiIndex if hiding the entire column headers
            row. Cannot be used simultaneously with ``subset``.

            .. versionadded:: 1.4.0
        names : bool
            Whether to hide the column index name(s), in the case all column headers,
            or some levels, are visible.

            .. versionadded:: 1.4.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.hide: Hide the entire index / columns, or specific rows / columns.
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.hide(axis='columns')`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.hide(axis=1, level=level, subset=subset, names=names)
