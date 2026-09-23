    @doc(
        _shared_docs["compare"],
        """
Returns
-------
Series or DataFrame
    If axis is 0 or 'index' the result will be a Series.
    The resulting index will be a MultiIndex with 'self' and 'other'
    stacked alternately at the inner level.

    If axis is 1 or 'columns' the result will be a DataFrame.
    It will have two columns namely 'self' and 'other'.

See Also
--------
DataFrame.compare : Compare with another DataFrame and show differences.

Notes
-----
Matching NaNs will not appear as a difference.

Examples
--------
>>> s1 = pd.Series(["a", "b", "c", "d", "e"])
>>> s2 = pd.Series(["a", "a", "c", "b", "e"])

Align the differences on columns

>>> s1.compare(s2)
  self other
1    b     a
3    d     b

Stack the differences on indices

>>> s1.compare(s2, align_axis=0)
1  self     b
   other    a
3  self     d
   other    b
dtype: object

Keep all original rows

>>> s1.compare(s2, keep_shape=True)
  self other
0  NaN   NaN
1    b     a
2  NaN   NaN
3    d     b
4  NaN   NaN

Keep all original rows and also all original values

>>> s1.compare(s2, keep_shape=True, keep_equal=True)
  self other
0    a     a
1    b     a
2    c     c
3    d     b
4    e     e
""",
        klass=_shared_doc_kwargs["klass"],
    )
    def compare(
        self,
        other: Series,
        align_axis: Axis = 1,
        keep_shape: bool = False,
        keep_equal: bool = False,
    ) -> DataFrame | Series:
        return super().compare(
            other=other,
            align_axis=align_axis,
            keep_shape=keep_shape,
            keep_equal=keep_equal,
        )
