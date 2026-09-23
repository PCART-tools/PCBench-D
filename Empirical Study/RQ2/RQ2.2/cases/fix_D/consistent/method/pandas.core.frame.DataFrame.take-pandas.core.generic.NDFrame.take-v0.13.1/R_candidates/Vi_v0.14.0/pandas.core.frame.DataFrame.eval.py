    def eval(self, expr, **kwargs):
        """Evaluate an expression in the context of the calling DataFrame
        instance.

        Parameters
        ----------
        expr : string
            The expression string to evaluate.
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
        resolvers = kwargs.pop('resolvers', None)
        kwargs['level'] = kwargs.pop('level', 0) + 1
        if resolvers is None:
            index_resolvers = self._get_index_resolvers()
            resolvers = dict(self.iteritems()), index_resolvers
        kwargs['target'] = self
        kwargs['resolvers'] = kwargs.get('resolvers', ()) + resolvers
        return _eval(expr, **kwargs)
