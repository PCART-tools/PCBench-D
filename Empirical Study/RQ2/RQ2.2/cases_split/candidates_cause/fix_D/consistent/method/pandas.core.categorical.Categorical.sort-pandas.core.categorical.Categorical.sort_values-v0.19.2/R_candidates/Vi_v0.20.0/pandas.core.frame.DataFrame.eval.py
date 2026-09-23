    def eval(self, expr, inplace=None, **kwargs):
        """Evaluate an expression in the context of the calling DataFrame
        instance.

        Parameters
        ----------
        expr : string
            The expression string to evaluate.
        inplace : bool
            If the expression contains an assignment, whether to return a new
            DataFrame or mutate the existing.

            WARNING: inplace=None currently falls back to to True, but
            in a future version, will default to False.  Use inplace=True
            explicitly rather than relying on the default.

            .. versionadded:: 0.18.0

        kwargs : dict
            See the documentation for :func:`~pandas.eval` for complete details
            on the keyword arguments accepted by
            :meth:`~pandas.DataFrame.query`.

        Returns
        -------
        ret : ndarray, scalar, or pandas object

        See Also
        --------
        pandas.DataFrame.query
        pandas.DataFrame.assign
        pandas.eval

        Notes
        -----
        For more details see the API documentation for :func:`~pandas.eval`.
        For detailed examples see :ref:`enhancing performance with eval
        <enhancingperf.eval>`.

        Examples
        --------
        >>> from numpy.random import randn
        >>> from pandas import DataFrame
        >>> df = DataFrame(randn(10, 2), columns=list('ab'))
        >>> df.eval('a + b')
        >>> df.eval('c = a + b')
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        resolvers = kwargs.pop('resolvers', None)
        kwargs['level'] = kwargs.pop('level', 0) + 1
        if resolvers is None:
            index_resolvers = self._get_index_resolvers()
            resolvers = dict(self.iteritems()), index_resolvers
        if 'target' not in kwargs:
            kwargs['target'] = self
        kwargs['resolvers'] = kwargs.get('resolvers', ()) + tuple(resolvers)
        return _eval(expr, inplace=inplace, **kwargs)
