    @doc(
        klass=_shared_doc_kwargs["klass"],
        cond="True",
        cond_rev="False",
        name="where",
        name_other="mask",
    )
    def where(
        self: NDFrameT,
        cond,
        other=np.nan,
        *,
        inplace: bool_t = False,
        axis: Axis | None = None,
        level: Level = None,
    ) -> NDFrameT | None:
        """
        Replace values where the condition is {cond_rev}.

        Parameters
        ----------
        cond : bool {klass}, array-like, or callable
            Where `cond` is {cond}, keep the original value. Where
            {cond_rev}, replace with corresponding value from `other`.
            If `cond` is callable, it is computed on the {klass} and
            should return boolean {klass} or array. The callable must
            not change input {klass} (though pandas doesn't check it).
        other : scalar, {klass}, or callable
            Entries where `cond` is {cond_rev} are replaced with
            corresponding value from `other`.
            If other is callable, it is computed on the {klass} and
            should return scalar or {klass}. The callable must not
            change input {klass} (though pandas doesn't check it).
            If not specified, entries will be filled with the corresponding
            NULL value (``np.nan`` for numpy dtypes, ``pd.NA`` for extension
            dtypes).
        inplace : bool, default False
            Whether to perform the operation in place on the data.
        axis : int, default None
            Alignment axis if needed. For `Series` this parameter is
            unused and defaults to 0.
        level : int, default None
            Alignment level if needed.

        Returns
        -------
        Same type as caller or None if ``inplace=True``.

        See Also
        --------
        :func:`DataFrame.{name_other}` : Return an object of same shape as
            self.

        Notes
        -----
        The {name} method is an application of the if-then idiom. For each
        element in the calling DataFrame, if ``cond`` is ``{cond}`` the
        element is used; otherwise the corresponding element from the DataFrame
        ``other`` is used. If the axis of ``other`` does not align with axis of
        ``cond`` {klass}, the misaligned index positions will be filled with
        {cond_rev}.

        The signature for :func:`DataFrame.where` differs from
        :func:`numpy.where`. Roughly ``df1.where(m, df2)`` is equivalent to
        ``np.where(m, df1, df2)``.

        For further details and examples see the ``{name}`` documentation in
        :ref:`indexing <indexing.where_mask>`.

        The dtype of the object takes precedence. The fill value is casted to
        the object's dtype, if this can be done losslessly.

        Examples
        --------
        >>> s = pd.Series(range(5))
        >>> s.where(s > 0)
        0    NaN
        1    1.0
        2    2.0
        3    3.0
        4    4.0
        dtype: float64
        >>> s.mask(s > 0)
        0    0.0
        1    NaN
        2    NaN
        3    NaN
        4    NaN
        dtype: float64

        >>> s = pd.Series(range(5))
        >>> t = pd.Series([True, False])
        >>> s.where(t, 99)
        0     0
        1    99
        2    99
        3    99
        4    99
        dtype: int64
        >>> s.mask(t, 99)
        0    99
        1     1
        2    99
        3    99
        4    99
        dtype: int64

        >>> s.where(s > 1, 10)
        0    10
        1    10
        2    2
        3    3
        4    4
        dtype: int64
        >>> s.mask(s > 1, 10)
        0     0
        1     1
        2    10
        3    10
        4    10
        dtype: int64

        >>> df = pd.DataFrame(np.arange(10).reshape(-1, 2), columns=['A', 'B'])
        >>> df
           A  B
        0  0  1
        1  2  3
        2  4  5
        3  6  7
        4  8  9
        >>> m = df % 3 == 0
        >>> df.where(m, -df)
           A  B
        0  0 -1
        1 -2  3
        2 -4 -5
        3  6 -7
        4 -8  9
        >>> df.where(m, -df) == np.where(m, df, -df)
              A     B
        0  True  True
        1  True  True
        2  True  True
        3  True  True
        4  True  True
        >>> df.where(m, -df) == df.mask(~m, -df)
              A     B
        0  True  True
        1  True  True
        2  True  True
        3  True  True
        4  True  True
        """
        other = common.apply_if_callable(other, self)
        return self._where(cond, other, inplace, axis, level)
