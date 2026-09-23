    @Substitution(subset=subset_args)
    def apply(
        self,
        func: Callable,
        axis: Axis | None = 0,
        subset: Subset | None = None,
        **kwargs,
    ) -> Styler:
        """
        Apply a CSS-styling function column-wise, row-wise, or table-wise.

        Updates the HTML representation with the result.

        Parameters
        ----------
        func : function
            ``func`` should take a Series if ``axis`` in [0,1] and return a list-like
            object of same length, or a Series, not necessarily of same length, with
            valid index labels considering ``subset``.
            ``func`` should take a DataFrame if ``axis`` is ``None`` and return either
            an ndarray with the same shape or a DataFrame, not necessarily of the same
            shape, with valid index and columns labels considering ``subset``.

            .. versionchanged:: 1.3.0

            .. versionchanged:: 1.4.0

        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        %(subset)s
        **kwargs : dict
            Pass along to ``func``.

        Returns
        -------
        Styler

        See Also
        --------
        Styler.map_index: Apply a CSS-styling function to headers elementwise.
        Styler.apply_index: Apply a CSS-styling function to headers level-wise.
        Styler.map: Apply a CSS-styling function elementwise.

        Notes
        -----
        The elements of the output of ``func`` should be CSS styles as strings, in the
        format 'attribute: value; attribute2: value2; ...' or,
        if nothing is to be applied to that element, an empty string or ``None``.

        This is similar to ``DataFrame.apply``, except that ``axis=None``
        applies the function to the entire DataFrame at once,
        rather than column-wise or row-wise.

        Examples
        --------
        >>> def highlight_max(x, color):
        ...     return np.where(x == np.nanmax(x.to_numpy()), f"color: {color};", None)
        >>> df = pd.DataFrame(np.random.randn(5, 2), columns=["A", "B"])
        >>> df.style.apply(highlight_max, color='red')  # doctest: +SKIP
        >>> df.style.apply(highlight_max, color='blue', axis=1)  # doctest: +SKIP
        >>> df.style.apply(highlight_max, color='green', axis=None)  # doctest: +SKIP

        Using ``subset`` to restrict application to a single column or multiple columns

        >>> df.style.apply(highlight_max, color='red', subset="A")
        ... # doctest: +SKIP
        >>> df.style.apply(highlight_max, color='red', subset=["A", "B"])
        ... # doctest: +SKIP

        Using a 2d input to ``subset`` to select rows in addition to columns

        >>> df.style.apply(highlight_max, color='red', subset=([0, 1, 2], slice(None)))
        ... # doctest: +SKIP
        >>> df.style.apply(highlight_max, color='red', subset=(slice(0, 5, 2), "A"))
        ... # doctest: +SKIP

        Using a function which returns a Series / DataFrame of unequal length but
        containing valid index labels

        >>> df = pd.DataFrame([[1, 2], [3, 4], [4, 6]], index=["A1", "A2", "Total"])
        >>> total_style = pd.Series("font-weight: bold;", index=["Total"])
        >>> df.style.apply(lambda s: total_style)  # doctest: +SKIP

        See `Table Visualization <../../user_guide/style.ipynb>`_ user guide for
        more details.
        """
        self._todo.append(
            (lambda instance: getattr(instance, "_apply"), (func, axis, subset), kwargs)
        )
        return self
