    def apply(
        self,
        func: Callable[..., Styler],
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
            ``func`` should take a Series if ``axis`` in [0,1] and return an object
            of same length, also with identical index if the object is a Series.
            ``func`` should take a DataFrame if ``axis`` is ``None`` and return either
            an ndarray with the same shape or a DataFrame with identical columns and
            index.

            .. versionchanged:: 1.3.0

        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        subset : label, array-like, IndexSlice, optional
            A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
            or single key, to `DataFrame.loc[:, <subset>]` where the columns are
            prioritised, to limit ``data`` to *before* applying the function.
        **kwargs : dict
            Pass along to ``func``.

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.applymap: Apply a CSS-styling function elementwise.

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
        >>> df.style.apply(highlight_max, color='red')
        >>> df.style.apply(highlight_max, color='blue', axis=1)
        >>> df.style.apply(highlight_max, color='green', axis=None)

        Using ``subset`` to restrict application to a single column or multiple columns

        >>> df.style.apply(highlight_max, color='red', subset="A")
        >>> df.style.apply(highlight_max, color='red', subset=["A", "B"])

        Using a 2d input to ``subset`` to select rows in addition to columns

        >>> df.style.apply(highlight_max, color='red', subset=([0,1,2], slice(None))
        >>> df.style.apply(highlight_max, color='red', subset=(slice(0,5,2), "A")
        """
        self._todo.append(
            (lambda instance: getattr(instance, "_apply"), (func, axis, subset), kwargs)
        )
        return self
