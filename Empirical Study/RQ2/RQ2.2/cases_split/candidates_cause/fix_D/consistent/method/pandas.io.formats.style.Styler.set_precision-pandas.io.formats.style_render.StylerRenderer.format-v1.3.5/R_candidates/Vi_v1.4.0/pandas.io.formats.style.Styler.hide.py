    def hide(
        self,
        subset: Subset | None = None,
        axis: Axis = 0,
        level: Level | list[Level] | None = None,
        names: bool = False,
    ) -> Styler:
        """
        Hide the entire index / column headers, or specific rows / columns from display.

        .. versionadded:: 1.4.0

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 1d input or single key along the axis within
            `DataFrame.loc[<subset>, :]` or `DataFrame.loc[:, <subset>]` depending
            upon ``axis``, to limit ``data`` to select hidden rows / columns.
        axis : {"index", 0, "columns", 1}
            Apply to the index or columns.
        level : int, str, list
            The level(s) to hide in a MultiIndex if hiding the entire index / column
            headers. Cannot be used simultaneously with ``subset``.
        names : bool
            Whether to hide the level name(s) of the index / columns headers in the case
            it (or at least one the levels) remains visible.

        Returns
        -------
        self : Styler

        Notes
        -----
        This method has multiple functionality depending upon the combination
        of the ``subset``, ``level`` and ``names`` arguments (see examples). The
        ``axis`` argument is used only to control whether the method is applied to row
        or column headers:

        .. list-table:: Argument combinations
           :widths: 10 20 10 60
           :header-rows: 1

           * - ``subset``
             - ``level``
             - ``names``
             - Effect
           * - None
             - None
             - False
             - The axis-Index is hidden entirely.
           * - None
             - None
             - True
             - Only the axis-Index names are hidden.
           * - None
             - Int, Str, List
             - False
             - Specified axis-MultiIndex levels are hidden entirely.
           * - None
             - Int, Str, List
             - True
             - Specified axis-MultiIndex levels are hidden entirely and the names of
               remaining axis-MultiIndex levels.
           * - Subset
             - None
             - False
             - The specified data rows/columns are hidden, but the axis-Index itself,
               and names, remain unchanged.
           * - Subset
             - None
             - True
             - The specified data rows/columns and axis-Index names are hidden, but
               the axis-Index itself remains unchanged.
           * - Subset
             - Int, Str, List
             - Boolean
             - ValueError: cannot supply ``subset`` and ``level`` simultaneously.

        Note this method only hides the identifed elements so can be chained to hide
        multiple elements in sequence.

        Examples
        --------
        Simple application hiding specific rows:

        >>> df = pd.DataFrame([[1,2], [3,4], [5,6]], index=["a", "b", "c"])
        >>> df.style.hide(["a", "b"])  # doctest: +SKIP
             0    1
        c    5    6

        Hide the index and retain the data values:

        >>> midx = pd.MultiIndex.from_product([["x", "y"], ["a", "b", "c"]])
        >>> df = pd.DataFrame(np.random.randn(6,6), index=midx, columns=midx)
        >>> df.style.format("{:.1f}").hide()  # doctest: +SKIP
                         x                    y
           a      b      c      a      b      c
         0.1    0.0    0.4    1.3    0.6   -1.4
         0.7    1.0    1.3    1.5   -0.0   -0.2
         1.4   -0.8    1.6   -0.2   -0.4   -0.3
         0.4    1.0   -0.2   -0.8   -1.2    1.1
        -0.6    1.2    1.8    1.9    0.3    0.3
         0.8    0.5   -0.3    1.2    2.2   -0.8

        Hide specific rows in a MultiIndex but retain the index:

        >>> df.style.format("{:.1f}").hide(subset=(slice(None), ["a", "c"]))
        ...   # doctest: +SKIP
                                 x                    y
                   a      b      c      a      b      c
        x   b    0.7    1.0    1.3    1.5   -0.0   -0.2
        y   b   -0.6    1.2    1.8    1.9    0.3    0.3

        Hide specific rows and the index through chaining:

        >>> df.style.format("{:.1f}").hide(subset=(slice(None), ["a", "c"])).hide()
        ...   # doctest: +SKIP
                         x                    y
           a      b      c      a      b      c
         0.7    1.0    1.3    1.5   -0.0   -0.2
        -0.6    1.2    1.8    1.9    0.3    0.3

        Hide a specific level:

        >>> df.style.format("{:,.1f}").hide(level=1)  # doctest: +SKIP
                             x                    y
               a      b      c      a      b      c
        x    0.1    0.0    0.4    1.3    0.6   -1.4
             0.7    1.0    1.3    1.5   -0.0   -0.2
             1.4   -0.8    1.6   -0.2   -0.4   -0.3
        y    0.4    1.0   -0.2   -0.8   -1.2    1.1
            -0.6    1.2    1.8    1.9    0.3    0.3
             0.8    0.5   -0.3    1.2    2.2   -0.8

        Hiding just the index level names:

        >>> df.index.names = ["lev0", "lev1"]
        >>> df.style.format("{:,.1f}").hide(names=True)  # doctest: +SKIP
                                 x                    y
                   a      b      c      a      b      c
        x   a    0.1    0.0    0.4    1.3    0.6   -1.4
            b    0.7    1.0    1.3    1.5   -0.0   -0.2
            c    1.4   -0.8    1.6   -0.2   -0.4   -0.3
        y   a    0.4    1.0   -0.2   -0.8   -1.2    1.1
            b   -0.6    1.2    1.8    1.9    0.3    0.3
            c    0.8    0.5   -0.3    1.2    2.2   -0.8

        Examples all produce equivalently transposed effects with ``axis="columns"``.
        """
        axis = self.data._get_axis_number(axis)
        if axis == 0:
            obj, objs, alt = "index", "index", "rows"
        else:
            obj, objs, alt = "column", "columns", "columns"

        if level is not None and subset is not None:
            raise ValueError("`subset` and `level` cannot be passed simultaneously")

        if subset is None:
            if level is None and names:
                # this combination implies user shows the index and hides just names
                setattr(self, f"hide_{obj}_names", True)
                return self

            levels_ = refactor_levels(level, getattr(self, objs))
            setattr(
                self,
                f"hide_{objs}_",
                [
                    True if lev in levels_ else False
                    for lev in range(getattr(self, objs).nlevels)
                ],
            )
        else:
            if axis == 0:
                subset_ = IndexSlice[subset, :]  # new var so mypy reads not Optional
            else:
                subset_ = IndexSlice[:, subset]  # new var so mypy reads not Optional
            subset = non_reducing_slice(subset_)
            hide = self.data.loc[subset]
            h_els = getattr(self, objs).get_indexer_for(getattr(hide, objs))
            setattr(self, f"hidden_{alt}", h_els)

        if names:
            setattr(self, f"hide_{obj}_names", True)
        return self
