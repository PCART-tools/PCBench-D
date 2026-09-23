    @Appender(
        """
        Examples
        --------
        >>> s = pd.Series([1, 2, 3])
        >>> s
        0    1
        1    2
        2    3
        dtype: int64

        >>> s.set_axis(['a', 'b', 'c'], axis=0)
        a    1
        b    2
        c    3
        dtype: int64
    """
    )
    @Substitution(
        **_shared_doc_kwargs,
        extended_summary_sub="",
        axis_description_sub="",
        see_also_sub="",
    )
    @Appender(NDFrame.set_axis.__doc__)
    def set_axis(
        self,
        labels,
        *,
        axis: Axis = 0,
        copy: bool | None = None,
    ) -> Series:
        return super().set_axis(labels, axis=axis, copy=copy)
