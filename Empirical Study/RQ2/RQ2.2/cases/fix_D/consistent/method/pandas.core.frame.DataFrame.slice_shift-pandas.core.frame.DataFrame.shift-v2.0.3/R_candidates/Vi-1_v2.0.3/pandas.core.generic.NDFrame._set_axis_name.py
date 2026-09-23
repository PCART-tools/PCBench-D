    @final
    def _set_axis_name(
        self, name, axis: Axis = 0, inplace: bool_t = False, copy: bool_t | None = True
    ):
        """
        Set the name(s) of the axis.

        Parameters
        ----------
        name : str or list of str
            Name(s) to set.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to set the label. The value 0 or 'index' specifies index,
            and the value 1 or 'columns' specifies columns.
        inplace : bool, default False
            If `True`, do operation inplace and return None.
        copy:
            Whether to make a copy of the result.

        Returns
        -------
        Series, DataFrame, or None
            The same type as the caller or `None` if `inplace` is `True`.

        See Also
        --------
        DataFrame.rename : Alter the axis labels of :class:`DataFrame`.
        Series.rename : Alter the index labels or set the index name
            of :class:`Series`.
        Index.rename : Set the name of :class:`Index` or :class:`MultiIndex`.

        Examples
        --------
        >>> df = pd.DataFrame({"num_legs": [4, 4, 2]},
        ...                   ["dog", "cat", "monkey"])
        >>> df
                num_legs
        dog            4
        cat            4
        monkey         2
        >>> df._set_axis_name("animal")
                num_legs
        animal
        dog            4
        cat            4
        monkey         2
        >>> df.index = pd.MultiIndex.from_product(
        ...                [["mammal"], ['dog', 'cat', 'monkey']])
        >>> df._set_axis_name(["type", "name"])
                       num_legs
        type   name
        mammal dog        4
               cat        4
               monkey     2
        """
        axis = self._get_axis_number(axis)
        idx = self._get_axis(axis).set_names(name)

        inplace = validate_bool_kwarg(inplace, "inplace")
        renamed = self if inplace else self.copy(deep=copy)
        if axis == 0:
            renamed.index = idx
        else:
            renamed.columns = idx

        if not inplace:
            return renamed
