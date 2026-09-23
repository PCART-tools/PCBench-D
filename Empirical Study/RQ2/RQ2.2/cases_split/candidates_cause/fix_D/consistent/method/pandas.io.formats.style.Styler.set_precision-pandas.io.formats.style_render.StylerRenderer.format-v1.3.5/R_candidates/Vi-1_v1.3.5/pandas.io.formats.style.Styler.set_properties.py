    def set_properties(self, subset: Subset | None = None, **kwargs) -> Styler:
        """
        Set defined CSS-properties to each ``<td>`` HTML element within the given
        subset.

        Parameters
        ----------
        subset : label, array-like, IndexSlice, optional
            A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
            or single key, to `DataFrame.loc[:, <subset>]` where the columns are
            prioritised, to limit ``data`` to *before* applying the function.
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
        >>> df.style.set_properties(color="white", align="right")
        >>> df.style.set_properties(**{'background-color': 'yellow'})
        """
        values = "".join(f"{p}: {v};" for p, v in kwargs.items())
        return self.applymap(lambda x: values, subset=subset)
