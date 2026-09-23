    def query(self, expr, **kwargs):
        """Query the columns of a frame with a boolean expression.

        Parameters
        ----------
        expr : string
            The query string to evaluate. The result of the evaluation of this
            expression is first passed to :attr:`~pandas.DataFrame.loc` and if
            that fails because of a multidimensional key (e.g., a DataFrame)
            then the result will be passed to
            :meth:`~pandas.DataFrame.__getitem__`.
        kwargs : dict
            See the documentation for :func:`~pandas.eval` for complete details
            on the keyword arguments accepted by
            :meth:`~pandas.DataFrame.query`.

        Returns
        -------
        q : DataFrame or Series

        Notes
        -----
        This method uses the top-level :func:`~pandas.eval` function to
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

        The :attr:`~pandas.DataFrame.index` and
        :attr:`~pandas.DataFrame.columns` attributes of the
        :class:`~pandas.DataFrame` instance is placed in the namespace by
        default, which allows you to treat both the index and columns of the
        frame as a column in the frame.
        The identifier ``index`` is used for this variable, and you can also
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
        # need to go up at least 4 stack frames
        # 4 expr.Scope
        # 3 expr._ensure_scope
        # 2 self.eval
        # 1 self.query
        # 0 self.query caller (implicit)
        level = kwargs.setdefault('level', 4)
        if level < 4:
            raise ValueError("Going up fewer than 4 stack frames will not"
                             " capture the necessary variable scope for a "
                             "query expression")

        res = self.eval(expr, **kwargs)

        try:
            return self.loc[res]
        except ValueError:
            # when res is multi-dimensional loc raises, but this is sometimes a
            # valid query
            return self[res]
