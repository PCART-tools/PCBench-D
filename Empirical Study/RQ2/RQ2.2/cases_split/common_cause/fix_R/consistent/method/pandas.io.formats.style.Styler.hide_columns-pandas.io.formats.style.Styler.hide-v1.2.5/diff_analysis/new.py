    def hide_columns(self, subset: Subset | None = None) -> Styler:
        """
        Hide the column headers or specific keys in the columns from rendering.

        This method has dual functionality:

          - if ``subset`` is ``None`` then the entire column headers row will be hidden
            whilst the data-values remain visible.
          - if a ``subset`` is given then those specific columns, including the
            data-values will be hidden, whilst the column headers row remains visible.

        .. versionchanged:: 1.3.0

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 1d input or single key along the columns axis within
            `DataFrame.loc[:, <subset>]`, to limit ``data`` to *before* applying
            the function.

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.hide_index: Hide the entire index, or specific keys in the index.

        Examples
        --------
        Simple application hiding specific columns:

        >>> df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["a", "b", "c"])
        >>> df.style.hide_columns(["a", "b"])
             c
        0    3
        1    6

        Hide column headers and retain the data values:

        >>> midx = pd.MultiIndex.from_product([["x", "y"], ["a", "b", "c"]])
        >>> df = pd.DataFrame(np.random.randn(6,6), index=midx, columns=midx)
        >>> df.style.format("{:.1f}").hide_columns()
        x   d    0.1    0.0    0.4    1.3    0.6   -1.4
            e    0.7    1.0    1.3    1.5   -0.0   -0.2
            f    1.4   -0.8    1.6   -0.2   -0.4   -0.3
        y   d    0.4    1.0   -0.2   -0.8   -1.2    1.1
            e   -0.6    1.2    1.8    1.9    0.3    0.3
            f    0.8    0.5   -0.3    1.2    2.2   -0.8

        Hide specific columns but retain the column headers:

        >>> df.style.format("{:.1f}").hide_columns(subset=(slice(None), ["a", "c"]))
                   x      y
                   b      b
        x   a    0.0    0.6
            b    1.0   -0.0
            c   -0.8   -0.4
        y   a    1.0   -1.2
            b    1.2    0.3
            c    0.5    2.2

        Hide specific columns and the column headers:

        >>> df.style.format("{:.1f}").hide_columns(subset=(slice(None), ["a", "c"]))
        ...     .hide_columns()
        x   a    0.0    0.6
            b    1.0   -0.0
            c   -0.8   -0.4
        y   a    1.0   -1.2
            b    1.2    0.3
            c    0.5    2.2
        """
        if subset is None:
            self.hide_columns_ = True
        else:
            subset_ = IndexSlice[:, subset]  # new var so mypy reads not Optional
            subset = non_reducing_slice(subset_)
            hide = self.data.loc[subset]
            hcols = self.columns.get_indexer_for(hide.columns)
            # error: Incompatible types in assignment (expression has type
            # "ndarray", variable has type "Sequence[int]")
            self.hidden_columns = hcols  # type: ignore[assignment]
        return self
