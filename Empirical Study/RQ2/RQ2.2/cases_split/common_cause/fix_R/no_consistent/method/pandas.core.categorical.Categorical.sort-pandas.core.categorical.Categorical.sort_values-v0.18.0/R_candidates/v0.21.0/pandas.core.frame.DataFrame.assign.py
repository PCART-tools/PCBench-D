    def assign(self, **kwargs):
        """
        Assign new columns to a DataFrame, returning a new object
        (a copy) with all the original columns in addition to the new ones.

        Parameters
        ----------
        kwargs : keyword, value pairs
            keywords are the column names. If the values are
            callable, they are computed on the DataFrame and
            assigned to the new columns. The callable must not
            change input DataFrame (though pandas doesn't check it).
            If the values are not callable, (e.g. a Series, scalar, or array),
            they are simply assigned.

        Returns
        -------
        df : DataFrame
            A new DataFrame with the new columns in addition to
            all the existing columns.

        Notes
        -----
        For python 3.6 and above, the columns are inserted in the order of
        \*\*kwargs. For python 3.5 and earlier, since \*\*kwargs is unordered,
        the columns are inserted in alphabetical order at the end of your
        DataFrame.  Assigning multiple columns within the same ``assign``
        is possible, but you cannot reference other columns created within
        the same ``assign`` call.

        Examples
        --------
        >>> df = DataFrame({'A': range(1, 11), 'B': np.random.randn(10)})

        Where the value is a callable, evaluated on `df`:

        >>> df.assign(ln_A = lambda x: np.log(x.A))
            A         B      ln_A
        0   1  0.426905  0.000000
        1   2 -0.780949  0.693147
        2   3 -0.418711  1.098612
        3   4 -0.269708  1.386294
        4   5 -0.274002  1.609438
        5   6 -0.500792  1.791759
        6   7  1.649697  1.945910
        7   8 -1.495604  2.079442
        8   9  0.549296  2.197225
        9  10 -0.758542  2.302585

        Where the value already exists and is inserted:

        >>> newcol = np.log(df['A'])
        >>> df.assign(ln_A=newcol)
            A         B      ln_A
        0   1  0.426905  0.000000
        1   2 -0.780949  0.693147
        2   3 -0.418711  1.098612
        3   4 -0.269708  1.386294
        4   5 -0.274002  1.609438
        5   6 -0.500792  1.791759
        6   7  1.649697  1.945910
        7   8 -1.495604  2.079442
        8   9  0.549296  2.197225
        9  10 -0.758542  2.302585
        """
        data = self.copy()

        # do all calculations first...
        results = OrderedDict()
        for k, v in kwargs.items():
            results[k] = com._apply_if_callable(v, data)

        # preserve order for 3.6 and later, but sort by key for 3.5 and earlier
        if PY36:
            results = results.items()
        else:
            results = sorted(results.items())
        # ... and then assign
        for k, v in results:
            data[k] = v
        return data
