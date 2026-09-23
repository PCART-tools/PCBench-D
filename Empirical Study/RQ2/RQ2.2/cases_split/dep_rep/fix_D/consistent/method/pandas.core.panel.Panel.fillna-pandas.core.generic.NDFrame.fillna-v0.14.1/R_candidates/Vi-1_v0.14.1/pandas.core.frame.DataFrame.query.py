    def query(self, expr, **kwargs):
        """Query the columns of a frame with a boolean expression.

        .. versionadded:: 0.13

        Parameters
        ----------
        expr : string
            The query string to evaluate.  You can refer to variables
            in the environment by prefixing them with an '@' character like
            ``@a + b``.
        kwargs : dict
            See the documentation for :func:`pandas.eval` for complete details
            on the keyword arguments accepted by :meth:`DataFrame.query`.

        Returns
        -------
        q : DataFrame

        Notes
        -----
        The result of the evaluation of this expression is first passed to
        :attr:`DataFrame.loc` and if that fails because of a
        multidimensional key (e.g., a DataFrame) then the result will be passed
        to :meth:`DataFrame.__getitem__`.

        This method uses the top-level :func:`pandas.eval` function to
        evaluate the passed query.

        The :meth:`~pandas.DataFrame.query` method uses a slightly
        modified Python syntax by default. For example, the ``&`` and ``|``
        (bitwise) operators have the precedence of their boolean cousins,
        :keyword:`and` and :keyword:`or`. This *is* syntactically valid Python,
        however the semantics are different.

        You can change the semantics of the expression by passing the keyword
        argument ``parser='python'``. This enforces the same semantics as
        evaluation in Python space. Likewise, you can pass ``engine='python'``
        to evaluate an expression using Python itself as a backend. This is not
        recommended as it is inefficient compared to using ``numexpr`` as the
        engine.

        The :attr:`DataFrame.index` and
        :attr:`DataFrame.columns` attributes of the
        :class:`~pandas.DataFrame` instance are placed in the query namespace
        by default, which allows you to treat both the index and columns of the
        frame as a column in the frame.
        The identifier ``index`` is used for the frame index; you can also
        use the name of the index to identify it in a query.

        For further details and examples see the ``query`` documentation in
        :ref:`indexing <indexing.query>`.

        See Also
        --------
        pandas.eval
        DataFrame.eval

        Examples
        --------
        >>> from numpy.random import randn
        >>> from pandas import DataFrame
        >>> df = DataFrame(randn(10, 2), columns=list('ab'))
        >>> df.query('a > b')
        >>> df[df.a > df.b]  # same result as the previous expression
        """
        kwargs['level'] = kwargs.pop('level', 0) + 1
        res = self.eval(expr, **kwargs)

        try:
            return self.loc[res]
        except ValueError:
            # when res is multi-dimensional loc raises, but this is sometimes a
            # valid query
            return self[res]
