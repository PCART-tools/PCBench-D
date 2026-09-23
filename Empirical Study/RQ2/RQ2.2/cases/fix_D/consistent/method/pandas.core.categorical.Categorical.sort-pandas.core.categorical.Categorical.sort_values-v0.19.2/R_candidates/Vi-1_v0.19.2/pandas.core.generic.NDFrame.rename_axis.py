    def rename_axis(self, mapper, axis=0, copy=True, inplace=False):
        """
        Alter index and / or columns using input function or functions.
        A scaler or list-like for ``mapper`` will alter the ``Index.name``
        or ``MultiIndex.names`` attribute.
        A function or dict for ``mapper`` will alter the labels.
        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is.

        Parameters
        ----------
        mapper : scalar, list-like, dict-like or function, optional
        axis : int or string, default 0
        copy : boolean, default True
            Also copy underlying data
        inplace : boolean, default False

        Returns
        -------
        renamed : type of caller

        See Also
        --------
        pandas.NDFrame.rename
        pandas.Index.rename

        Examples
        --------
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> df.rename_axis("foo")  # scalar, alters df.index.name
             A  B
        foo
        0    1  4
        1    2  5
        2    3  6
        >>> df.rename_axis(lambda x: 2 * x)  # function: alters labels
           A  B
        0  1  4
        2  2  5
        4  3  6
        >>> df.rename_axis({"A": "ehh", "C": "see"}, axis="columns")  # mapping
           ehh  B
        0    1  4
        1    2  5
        2    3  6
        """
        non_mapper = is_scalar(mapper) or (is_list_like(mapper) and not
                                           is_dict_like(mapper))
        if non_mapper:
            return self._set_axis_name(mapper, axis=axis)
        else:
            axis = self._get_axis_name(axis)
            d = {'copy': copy, 'inplace': inplace}
            d[axis] = mapper
            return self.rename(**d)
