    @classmethod
    def from_records(
        cls,
        data,
        index=None,
        exclude=None,
        columns=None,
        coerce_float: bool = False,
        nrows: int | None = None,
    ) -> DataFrame:
        """
        Convert structured or record ndarray to DataFrame.

        Creates a DataFrame object from a structured ndarray, sequence of
        tuples or dicts, or DataFrame.

        Parameters
        ----------
        data : structured ndarray, sequence of tuples or dicts, or DataFrame
            Structured input data.
        index : str, list of fields, array-like
            Field of array to use as the index, alternately a specific set of
            input labels to use.
        exclude : sequence, default None
            Columns or fields to exclude.
        columns : sequence, default None
            Column names to use. If the passed data do not have names
            associated with them, this argument provides names for the
            columns. Otherwise this argument indicates the order of the columns
            in the result (any names not found in the data will become all-NA
            columns).
        coerce_float : bool, default False
            Attempt to convert values of non-string, non-numeric objects (like
            decimal.Decimal) to floating point, useful for SQL result sets.
        nrows : int, default None
            Number of rows to read if data is an iterator.

        Returns
        -------
        DataFrame

        See Also
        --------
        DataFrame.from_dict : DataFrame from dict of array-like or dicts.
        DataFrame : DataFrame object creation using constructor.

        Examples
        --------
        Data can be provided as a structured ndarray:

        >>> data = np.array([(3, 'a'), (2, 'b'), (1, 'c'), (0, 'd')],
        ...                 dtype=[('col_1', 'i4'), ('col_2', 'U1')])
        >>> pd.DataFrame.from_records(data)
           col_1 col_2
        0      3     a
        1      2     b
        2      1     c
        3      0     d

        Data can be provided as a list of dicts:

        >>> data = [{'col_1': 3, 'col_2': 'a'},
        ...         {'col_1': 2, 'col_2': 'b'},
        ...         {'col_1': 1, 'col_2': 'c'},
        ...         {'col_1': 0, 'col_2': 'd'}]
        >>> pd.DataFrame.from_records(data)
           col_1 col_2
        0      3     a
        1      2     b
        2      1     c
        3      0     d

        Data can be provided as a list of tuples with corresponding columns:

        >>> data = [(3, 'a'), (2, 'b'), (1, 'c'), (0, 'd')]
        >>> pd.DataFrame.from_records(data, columns=['col_1', 'col_2'])
           col_1 col_2
        0      3     a
        1      2     b
        2      1     c
        3      0     d
        """
        if isinstance(data, DataFrame):
            if columns is not None:
                if is_scalar(columns):
                    columns = [columns]
                data = data[columns]
            if index is not None:
                data = data.set_index(index)
            if exclude is not None:
                data = data.drop(columns=exclude)
            return data.copy(deep=False)

        result_index = None

        # Make a copy of the input columns so we can modify it
        if columns is not None:
            columns = ensure_index(columns)

        def maybe_reorder(
            arrays: list[ArrayLike], arr_columns: Index, columns: Index, index
        ) -> tuple[list[ArrayLike], Index, Index | None]:
            """
            If our desired 'columns' do not match the data's pre-existing 'arr_columns',
            we re-order our arrays.  This is like a pre-emptive (cheap) reindex.
            """
            if len(arrays):
                length = len(arrays[0])
            else:
                length = 0

            result_index = None
            if len(arrays) == 0 and index is None and length == 0:
                result_index = default_index(0)

            arrays, arr_columns = reorder_arrays(arrays, arr_columns, columns, length)
            return arrays, arr_columns, result_index

        if is_iterator(data):
            if nrows == 0:
                return cls()

            try:
                first_row = next(data)
            except StopIteration:
                return cls(index=index, columns=columns)

            dtype = None
            if hasattr(first_row, "dtype") and first_row.dtype.names:
                dtype = first_row.dtype

            values = [first_row]

            if nrows is None:
                values += data
            else:
                values.extend(itertools.islice(data, nrows - 1))

            if dtype is not None:
                data = np.array(values, dtype=dtype)
            else:
                data = values

        if isinstance(data, dict):
            if columns is None:
                columns = arr_columns = ensure_index(sorted(data))
                arrays = [data[k] for k in columns]
            else:
                arrays = []
                arr_columns_list = []
                for k, v in data.items():
                    if k in columns:
                        arr_columns_list.append(k)
                        arrays.append(v)

                arr_columns = Index(arr_columns_list)
                arrays, arr_columns, result_index = maybe_reorder(
                    arrays, arr_columns, columns, index
                )

        elif isinstance(data, (np.ndarray, DataFrame)):
            arrays, columns = to_arrays(data, columns)
            arr_columns = columns
        else:
            arrays, arr_columns = to_arrays(data, columns)
            if coerce_float:
                for i, arr in enumerate(arrays):
                    if arr.dtype == object:
                        # error: Argument 1 to "maybe_convert_objects" has
                        # incompatible type "Union[ExtensionArray, ndarray]";
                        # expected "ndarray"
                        arrays[i] = lib.maybe_convert_objects(
                            arr,  # type: ignore[arg-type]
                            try_float=True,
                        )

            arr_columns = ensure_index(arr_columns)
            if columns is None:
                columns = arr_columns
            else:
                arrays, arr_columns, result_index = maybe_reorder(
                    arrays, arr_columns, columns, index
                )

        if exclude is None:
            exclude = set()
        else:
            exclude = set(exclude)

        if index is not None:
            if isinstance(index, str) or not hasattr(index, "__iter__"):
                i = columns.get_loc(index)
                exclude.add(index)
                if len(arrays) > 0:
                    result_index = Index(arrays[i], name=index)
                else:
                    result_index = Index([], name=index)
            else:
                try:
                    index_data = [arrays[arr_columns.get_loc(field)] for field in index]
                except (KeyError, TypeError):
                    # raised by get_loc, see GH#29258
                    result_index = index
                else:
                    result_index = ensure_index_from_sequences(index_data, names=index)
                    exclude.update(index)

        if any(exclude):
            arr_exclude = [x for x in exclude if x in arr_columns]
            to_remove = [arr_columns.get_loc(col) for col in arr_exclude]
            arrays = [v for i, v in enumerate(arrays) if i not in to_remove]

            columns = columns.drop(exclude)

        manager = get_option("mode.data_manager")
        mgr = arrays_to_mgr(arrays, columns, result_index, typ=manager)

        return cls(mgr)
