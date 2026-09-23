    def to_frame(self, index: bool = True, name=None) -> DataFrame:
        """
        Create a DataFrame with the levels of the MultiIndex as columns.

        Column ordering is determined by the DataFrame constructor with data as
        a dict.

        Parameters
        ----------
        index : bool, default True
            Set the index of the returned DataFrame as the original MultiIndex.

        name : list / sequence of str, optional
            The passed names should substitute index level names.

        Returns
        -------
        DataFrame : a DataFrame containing the original MultiIndex data.

        See Also
        --------
        DataFrame : Two-dimensional, size-mutable, potentially heterogeneous
            tabular data.

        Examples
        --------
        >>> mi = pd.MultiIndex.from_arrays([['a', 'b'], ['c', 'd']])
        >>> mi
        MultiIndex([('a', 'c'),
                    ('b', 'd')],
                   )

        >>> df = mi.to_frame()
        >>> df
             0  1
        a c  a  c
        b d  b  d

        >>> df = mi.to_frame(index=False)
        >>> df
           0  1
        0  a  c
        1  b  d

        >>> df = mi.to_frame(name=['x', 'y'])
        >>> df
             x  y
        a c  a  c
        b d  b  d
        """
        from pandas import DataFrame

        if name is not None:
            if not is_list_like(name):
                raise TypeError("'name' must be a list / sequence of column names.")

            if len(name) != len(self.levels):
                raise ValueError(
                    "'name' should have same length as number of levels on index."
                )
            idx_names = name
        else:
            idx_names = self.names

        # Guarantee resulting column order - PY36+ dict maintains insertion order
        result = DataFrame(
            {
                (level if lvlname is None else lvlname): self._get_level_values(level)
                for lvlname, level in zip(idx_names, range(len(self.levels)))
            },
            copy=False,
        )

        if index:
            result.index = self
        return result
