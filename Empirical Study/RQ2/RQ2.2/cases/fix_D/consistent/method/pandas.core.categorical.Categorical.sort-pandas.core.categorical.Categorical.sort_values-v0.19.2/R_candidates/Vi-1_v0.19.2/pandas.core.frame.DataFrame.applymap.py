    def applymap(self, func):
        """
        Apply a function to a DataFrame that is intended to operate
        elementwise, i.e. like doing map(func, series) for each series in the
        DataFrame

        Parameters
        ----------
        func : function
            Python function, returns a single value from a single value

        Examples
        --------

        >>> df = pd.DataFrame(np.random.randn(3, 3))
        >>> df
            0         1          2
        0  -0.029638  1.081563   1.280300
        1   0.647747  0.831136  -1.549481
        2   0.513416 -0.884417   0.195343
        >>> df = df.applymap(lambda x: '%.2f' % x)
        >>> df
            0         1          2
        0  -0.03      1.08       1.28
        1   0.65      0.83      -1.55
        2   0.51     -0.88       0.20

        Returns
        -------
        applied : DataFrame

        See also
        --------
        DataFrame.apply : For operations on rows/columns

        """

        # if we have a dtype == 'M8[ns]', provide boxed values
        def infer(x):
            return lib.map_infer(x.asobject, func)

        return self.apply(infer)
