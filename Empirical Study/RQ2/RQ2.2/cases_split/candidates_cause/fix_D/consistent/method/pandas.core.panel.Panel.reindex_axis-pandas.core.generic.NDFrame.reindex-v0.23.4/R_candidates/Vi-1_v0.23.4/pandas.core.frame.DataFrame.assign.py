    def assign(self, **kwargs):
        r"""
        Assign new columns to a DataFrame, returning a new object
        (a copy) with the new columns added to the original ones.
        Existing columns that are re-assigned will be overwritten.

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
        Assigning multiple columns within the same ``assign`` is possible.
        For Python 3.6 and above, later items in '\*\*kwargs' may refer to
        newly created or modified columns in 'df'; items are computed and
        assigned into 'df' in order.  For Python 3.5 and below, the order of
        keyword arguments is not specified, you cannot refer to newly created
        or modified columns. All items are computed first, and then assigned
        in alphabetical order.

        .. versionchanged :: 0.23.0

            Keyword argument order is maintained for Python 3.6 and later.

        Examples
        --------
        >>> df = pd.DataFrame({'A': range(1, 11), 'B': np.random.randn(10)})

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

        Where the keyword arguments depend on each other

        >>> df = pd.DataFrame({'A': [1, 2, 3]})

        >>> df.assign(B=df.A, C=lambda x:x['A']+ x['B'])
            A  B  C
         0  1  1  2
         1  2  2  4
         2  3  3  6
        """
        data = self.copy()

        # >= 3.6 preserve order of kwargs
        if PY36:
            for k, v in kwargs.items():
                data[k] = com._apply_if_callable(v, data)
        else:
            # <= 3.5: do all calculations first...
            results = OrderedDict()
            for k, v in kwargs.items():
                results[k] = com._apply_if_callable(v, data)

            # <= 3.5 and earlier
            results = sorted(results.items())
            # ... and then assign
            for k, v in results:
                data[k] = v
        return data
