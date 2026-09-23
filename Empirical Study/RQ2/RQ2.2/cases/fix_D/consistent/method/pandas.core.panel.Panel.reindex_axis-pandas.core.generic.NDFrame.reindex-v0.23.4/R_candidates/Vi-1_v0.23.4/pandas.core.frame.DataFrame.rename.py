    @rewrite_axis_style_signature('mapper', [('copy', True),
                                             ('inplace', False),
                                             ('level', None)])
    def rename(self, *args, **kwargs):
        """Alter axes labels.

        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is. Extra labels listed don't throw an
        error.

        See the :ref:`user guide <basics.rename>` for more.

        Parameters
        ----------
        mapper, index, columns : dict-like or function, optional
            dict-like or functions transformations to apply to
            that axis' values. Use either ``mapper`` and ``axis`` to
            specify the axis to target with ``mapper``, or ``index`` and
            ``columns``.
        axis : int or str, optional
            Axis to target with ``mapper``. Can be either the axis name
            ('index', 'columns') or number (0, 1). The default is 'index'.
        copy : boolean, default True
            Also copy underlying data
        inplace : boolean, default False
            Whether to return a new DataFrame. If True then value of copy is
            ignored.
        level : int or level name, default None
            In case of a MultiIndex, only rename labels in the specified
            level.

        Returns
        -------
        renamed : DataFrame

        See Also
        --------
        pandas.DataFrame.rename_axis

        Examples
        --------

        ``DataFrame.rename`` supports two calling conventions

        * ``(index=index_mapper, columns=columns_mapper, ...)``
        * ``(mapper, axis={'index', 'columns'}, ...)``

        We *highly* recommend using keyword arguments to clarify your
        intent.

        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> df.rename(index=str, columns={"A": "a", "B": "c"})
           a  c
        0  1  4
        1  2  5
        2  3  6

        >>> df.rename(index=str, columns={"A": "a", "C": "c"})
           a  B
        0  1  4
        1  2  5
        2  3  6

        Using axis-style parameters

        >>> df.rename(str.lower, axis='columns')
           a  b
        0  1  4
        1  2  5
        2  3  6

        >>> df.rename({1: 2, 2: 4}, axis='index')
           A  B
        0  1  4
        2  2  5
        4  3  6
        """
        axes = validate_axis_style_args(self, args, kwargs, 'mapper', 'rename')
        kwargs.update(axes)
        # Pop these, since the values are in `kwargs` under different names
        kwargs.pop('axis', None)
        kwargs.pop('mapper', None)
        return super(DataFrame, self).rename(**kwargs)
