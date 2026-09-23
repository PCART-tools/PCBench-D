    def hide_index(
        self,
        subset: Subset | None = None,
        level: Level | list[Level] | None = None,
        names: bool = False,
    ) -> Styler:
        """
        Hide the entire index, or specific keys in the index from rendering.

        This method has dual functionality:

          - if ``subset`` is ``None`` then the entire index, or specified levels, will
            be hidden whilst displaying all data-rows.
          - if a ``subset`` is given then those specific rows will be hidden whilst the
            index itself remains visible.

        .. versionchanged:: 1.3.0

        .. deprecated:: 1.4.0
           This method should be replaced by ``hide(axis="index", **kwargs)``

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 1d input or single key along the index axis within
            `DataFrame.loc[<subset>, :]`, to limit ``data`` to *before* applying
            the function.
        level : int, str, list
            The level(s) to hide in a MultiIndex if hiding the entire index. Cannot be
            used simultaneously with ``subset``.

            .. versionadded:: 1.4.0
        names : bool
            Whether to hide the index name(s), in the case the index or part of it
            remains visible.

            .. versionadded:: 1.4.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.hide: Hide the entire index / columns, or specific rows / columns.
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.hide(axis='index')`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.hide(axis=0, level=level, subset=subset, names=names)
