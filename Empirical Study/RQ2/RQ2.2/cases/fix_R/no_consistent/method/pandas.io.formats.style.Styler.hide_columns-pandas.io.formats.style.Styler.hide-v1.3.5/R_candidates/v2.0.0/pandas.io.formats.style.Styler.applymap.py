    @Substitution(subset=subset_args)
    def applymap(
        self, func: Callable, subset: Subset | None = None, **kwargs
    ) -> Styler:
        """
        Apply a CSS-styling function elementwise.

        Updates the HTML representation with the result.

        Parameters
        ----------
        func : function
            ``func`` should take a scalar and return a string.
        %(subset)s
        **kwargs : dict
            Pass along to ``func``.

        Returns
        -------
        Styler

        See Also
        --------
        Styler.applymap_index: Apply a CSS-styling function to headers elementwise.
        Styler.apply_index: Apply a CSS-styling function to headers level-wise.
        Styler.apply: Apply a CSS-styling function column-wise, row-wise, or table-wise.

        Notes
        -----
        The elements of the output of ``func`` should be CSS styles as strings, in the
        format 'attribute: value; attribute2: value2; ...' or,
        if nothing is to be applied to that element, an empty string or ``None``.

        Examples
        --------
        >>> def color_negative(v, color):
        ...     return f"color: {color};" if v < 0 else None
        >>> df = pd.DataFrame(np.random.randn(5, 2), columns=["A", "B"])
        >>> df.style.applymap(color_negative, color='red')  # doctest: +SKIP

        Using ``subset`` to restrict application to a single column or multiple columns

        >>> df.style.applymap(color_negative, color='red', subset="A")
        ...  # doctest: +SKIP
        >>> df.style.applymap(color_negative, color='red', subset=["A", "B"])
        ...  # doctest: +SKIP

        Using a 2d input to ``subset`` to select rows in addition to columns

        >>> df.style.applymap(color_negative, color='red',
        ...  subset=([0,1,2], slice(None)))  # doctest: +SKIP
        >>> df.style.applymap(color_negative, color='red', subset=(slice(0,5,2), "A"))
        ...  # doctest: +SKIP

        See `Table Visualization <../../user_guide/style.ipynb>`_ user guide for
        more details.
        """
        self._todo.append(
            (lambda instance: getattr(instance, "_applymap"), (func, subset), kwargs)
        )
        return self
