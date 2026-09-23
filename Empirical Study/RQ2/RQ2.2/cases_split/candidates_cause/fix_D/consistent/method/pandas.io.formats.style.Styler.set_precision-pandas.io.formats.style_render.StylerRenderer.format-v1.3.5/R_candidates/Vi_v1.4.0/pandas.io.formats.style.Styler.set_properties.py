    @Substitution(subset=subset)
    def set_properties(self, subset: Subset | None = None, **kwargs) -> Styler:
        """
        Set defined CSS-properties to each ``<td>`` HTML element within the given
        subset.

        Parameters
        ----------
        %(subset)s
        **kwargs : dict
            A dictionary of property, value pairs to be set for each cell.

        Returns
        -------
        self : Styler

        Notes
        -----
        This is a convenience methods which wraps the :meth:`Styler.applymap` calling a
        function returning the CSS-properties independently of the data.

        Examples
        --------
        >>> df = pd.DataFrame(np.random.randn(10, 4))
        >>> df.style.set_properties(color="white", align="right")  # doctest: +SKIP
        >>> df.style.set_properties(**{'background-color': 'yellow'})  # doctest: +SKIP

        See `Table Visualization <../../user_guide/style.ipynb>`_ user guide for
        more details.
        """
        values = "".join([f"{p}: {v};" for p, v in kwargs.items()])
        return self.applymap(lambda x: values, subset=subset)
