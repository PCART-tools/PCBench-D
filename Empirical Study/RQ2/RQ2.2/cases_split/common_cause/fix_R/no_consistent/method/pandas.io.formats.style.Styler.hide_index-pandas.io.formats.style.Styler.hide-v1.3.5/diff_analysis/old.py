    def hide_index(self, subset: Subset | None = None) -> Styler:
        """
        Hide the entire index, or specific keys in the index from rendering.

        This method has dual functionality:

          - if ``subset`` is ``None`` then the entire index will be hidden whilst
            displaying all data-rows.
          - if a ``subset`` is given then those specific rows will be hidden whilst the
            index itself remains visible.

        .. versionchanged:: 1.3.0

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 1d input or single key along the index axis within
            `DataFrame.loc[<subset>, :]`, to limit ``data`` to *before* applying
            the function.

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.hide_columns: Hide the entire column headers row, or specific columns.

        Examples
        --------
        Simple application hiding specific rows:

        >>> df = pd.DataFrame([[1,2], [3,4], [5,6]], index=["a", "b", "c"])
        >>> df.style.hide_index(["a", "b"])
             0    1
        c    5    6

        Hide the index and retain the data values:

        >>> midx = pd.MultiIndex.from_product([["x", "y"], ["a", "b", "c"]])
        >>> df = pd.DataFrame(np.random.randn(6,6), index=midx, columns=midx)
        >>> df.style.format("{:.1f}").hide_index()
                         x                    y
           a      b      c      a      b      c
         0.1    0.0    0.4    1.3    0.6   -1.4
         0.7    1.0    1.3    1.5   -0.0   -0.2
         1.4   -0.8    1.6   -0.2   -0.4   -0.3
         0.4    1.0   -0.2   -0.8   -1.2    1.1
        -0.6    1.2    1.8    1.9    0.3    0.3
         0.8    0.5   -0.3    1.2    2.2   -0.8

        Hide specific rows but retain the index:

        >>> df.style.format("{:.1f}").hide_index(subset=(slice(None), ["a", "c"]))
                                 x                    y
                   a      b      c      a      b      c
        x   b    0.7    1.0    1.3    1.5   -0.0   -0.2
        y   b   -0.6    1.2    1.8    1.9    0.3    0.3

        Hide specific rows and the index:

        >>> df.style.format("{:.1f}").hide_index(subset=(slice(None), ["a", "c"]))
        ...     .hide_index()
                         x                    y
           a      b      c      a      b      c
         0.7    1.0    1.3    1.5   -0.0   -0.2
        -0.6    1.2    1.8    1.9    0.3    0.3
        """
        if subset is None:
            self.hide_index_ = True
        else:
            subset_ = IndexSlice[subset, :]  # new var so mypy reads not Optional
            subset = non_reducing_slice(subset_)
            hide = self.data.loc[subset]
            hrows = self.index.get_indexer_for(hide.index)
            # error: Incompatible types in assignment (expression has type
            # "ndarray", variable has type "Sequence[int]")
            self.hidden_rows = hrows  # type: ignore[assignment]
        return self
