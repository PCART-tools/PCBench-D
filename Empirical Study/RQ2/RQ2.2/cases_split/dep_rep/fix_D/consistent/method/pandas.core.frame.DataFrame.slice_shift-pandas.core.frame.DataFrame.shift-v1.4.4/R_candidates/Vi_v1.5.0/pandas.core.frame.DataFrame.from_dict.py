    @classmethod
    def from_dict(
        cls,
        data: dict,
        orient: str = "columns",
        dtype: Dtype | None = None,
        columns: Axes | None = None,
    ) -> DataFrame:
        """
        Construct DataFrame from dict of array-like or dicts.

        Creates DataFrame object from dictionary by columns or by index
        allowing dtype specification.

        Parameters
        ----------
        data : dict
            Of the form {field : array-like} or {field : dict}.
        orient : {'columns', 'index', 'tight'}, default 'columns'
            The "orientation" of the data. If the keys of the passed dict
            should be the columns of the resulting DataFrame, pass 'columns'
            (default). Otherwise if the keys should be rows, pass 'index'.
            If 'tight', assume a dict with keys ['index', 'columns', 'data',
            'index_names', 'column_names'].

            .. versionadded:: 1.4.0
               'tight' as an allowed value for the ``orient`` argument

        dtype : dtype, default None
            Data type to force, otherwise infer.
        columns : list, default None
            Column labels to use when ``orient='index'``. Raises a ValueError
            if used with ``orient='columns'`` or ``orient='tight'``.

        Returns
        -------
        DataFrame

        See Also
        --------
        DataFrame.from_records : DataFrame from structured ndarray, sequence
            of tuples or dicts, or DataFrame.
        DataFrame : DataFrame object creation using constructor.
        DataFrame.to_dict : Convert the DataFrame to a dictionary.

        Examples
        --------
        By default the keys of the dict become the DataFrame columns:

        >>> data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
        >>> pd.DataFrame.from_dict(data)
           col_1 col_2
        0      3     a
        1      2     b
        2      1     c
        3      0     d

        Specify ``orient='index'`` to create the DataFrame using dictionary
        keys as rows:

        >>> data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
        >>> pd.DataFrame.from_dict(data, orient='index')
               0  1  2  3
        row_1  3  2  1  0
        row_2  a  b  c  d

        When using the 'index' orientation, the column names can be
        specified manually:

        >>> pd.DataFrame.from_dict(data, orient='index',
        ...                        columns=['A', 'B', 'C', 'D'])
               A  B  C  D
        row_1  3  2  1  0
        row_2  a  b  c  d

        Specify ``orient='tight'`` to create the DataFrame using a 'tight'
        format:

        >>> data = {'index': [('a', 'b'), ('a', 'c')],
        ...         'columns': [('x', 1), ('y', 2)],
        ...         'data': [[1, 3], [2, 4]],
        ...         'index_names': ['n1', 'n2'],
        ...         'column_names': ['z1', 'z2']}
        >>> pd.DataFrame.from_dict(data, orient='tight')
        z1     x  y
        z2     1  2
        n1 n2
        a  b   1  3
           c   2  4
        """
        index = None
        orient = orient.lower()
        if orient == "index":
            if len(data) > 0:
                # TODO speed up Series case
                if isinstance(list(data.values())[0], (Series, dict)):
                    data = _from_nested_dict(data)
                else:
                    index = list(data.keys())
                    # error: Incompatible types in assignment (expression has type
                    # "List[Any]", variable has type "Dict[Any, Any]")
                    data = list(data.values())  # type: ignore[assignment]
        elif orient == "columns" or orient == "tight":
            if columns is not None:
                raise ValueError(f"cannot use columns parameter with orient='{orient}'")
        else:  # pragma: no cover
            raise ValueError(
                f"Expected 'index', 'columns' or 'tight' for orient parameter. "
                f"Got '{orient}' instead"
            )

        if orient != "tight":
            return cls(data, index=index, columns=columns, dtype=dtype)
        else:
            realdata = data["data"]

            def create_index(indexlist, namelist):
                index: Index
                if len(namelist) > 1:
                    index = MultiIndex.from_tuples(indexlist, names=namelist)
                else:
                    index = Index(indexlist, name=namelist[0])
                return index

            index = create_index(data["index"], data["index_names"])
            columns = create_index(data["columns"], data["column_names"])
            return cls(realdata, index=index, columns=columns, dtype=dtype)
