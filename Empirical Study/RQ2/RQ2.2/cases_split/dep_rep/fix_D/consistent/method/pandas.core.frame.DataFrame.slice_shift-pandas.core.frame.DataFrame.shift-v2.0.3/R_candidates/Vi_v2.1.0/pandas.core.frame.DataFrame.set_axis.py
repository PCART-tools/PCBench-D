    @Appender(
        """
        Examples
        --------
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        Change the row labels.

        >>> df.set_axis(['a', 'b', 'c'], axis='index')
           A  B
        a  1  4
        b  2  5
        c  3  6

        Change the column labels.

        >>> df.set_axis(['I', 'II'], axis='columns')
           I  II
        0  1   4
        1  2   5
        2  3   6
        """
    )
    @Substitution(
        klass=_shared_doc_kwargs["klass"],
        axes_single_arg=_shared_doc_kwargs["axes_single_arg"],
        extended_summary_sub=" column or",
        axis_description_sub=", and 1 identifies the columns",
        see_also_sub=" or columns",
    )
    @Appender(NDFrame.set_axis.__doc__)
    def set_axis(
        self,
        labels,
        *,
        axis: Axis = 0,
        copy: bool | None = None,
    ) -> DataFrame:
        return super().set_axis(labels, axis=axis, copy=copy)
