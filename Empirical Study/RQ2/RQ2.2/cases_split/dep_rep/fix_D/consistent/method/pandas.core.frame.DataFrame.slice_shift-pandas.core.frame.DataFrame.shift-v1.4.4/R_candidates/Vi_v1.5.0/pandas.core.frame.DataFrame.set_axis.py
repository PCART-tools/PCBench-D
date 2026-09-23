    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "labels"])
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

        Now, update the labels without copying the underlying data.

        >>> df.set_axis(['i', 'ii'], axis='columns', copy=False)
           i  ii
        0  1   4
        1  2   5
        2  3   6
        """
    )
    @Substitution(
        **_shared_doc_kwargs,
        extended_summary_sub=" column or",
        axis_description_sub=", and 1 identifies the columns",
        see_also_sub=" or columns",
    )
    @Appender(NDFrame.set_axis.__doc__)
    def set_axis(
        self,
        labels,
        axis: Axis = 0,
        inplace: bool | lib.NoDefault = lib.no_default,
        *,
        copy: bool | lib.NoDefault = lib.no_default,
    ):
        return super().set_axis(labels, axis=axis, inplace=inplace, copy=copy)
