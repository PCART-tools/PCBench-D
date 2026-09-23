    def to_frame(self, index=True, name=None):
        """
        Create a DataFrame with the levels of the MultiIndex as columns.

        Column ordering is determined by the DataFrame constructor with data as
        a dict.

        .. versionadded:: 0.24.0

        Parameters
        ----------
        index : boolean, default True
            Set the index of the returned DataFrame as the original MultiIndex.

        name : list / sequence of strings, optional
            The passed names should substitute index level names.

        Returns
        -------
        DataFrame : a DataFrame containing the original MultiIndex data.

        See Also
        --------
        DataFrame
        """

        from pandas import DataFrame

        if name is not None:
            if not is_list_like(name):
                raise TypeError("'name' must be a list / sequence " "of column names.")

            if len(name) != len(self.levels):
                raise ValueError(
                    "'name' should have same length as " "number of levels on index."
                )
            idx_names = name
        else:
            idx_names = self.names

        # Guarantee resulting column order
        result = DataFrame(
            OrderedDict(
                [
                    (
                        (level if lvlname is None else lvlname),
                        self._get_level_values(level),
                    )
                    for lvlname, level in zip(idx_names, range(len(self.levels)))
                ]
            ),
            copy=False,
        )

        if index:
            result.index = self
        return result
