    def to_dict(self, orient: str = "dict", into=dict):
        """
        Convert the DataFrame to a dictionary.

        The type of the key-value pairs can be customized with the parameters
        (see below).

        Parameters
        ----------
        orient : str {'dict', 'list', 'series', 'split', 'records', 'index'}
            Determines the type of the values of the dictionary.

            - 'dict' (default) : dict like {column -> {index -> value}}
            - 'list' : dict like {column -> [values]}
            - 'series' : dict like {column -> Series(values)}
            - 'split' : dict like
              {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}
            - 'tight' : dict like
              {'index' -> [index], 'columns' -> [columns], 'data' -> [values],
              'index_names' -> [index.names], 'column_names' -> [column.names]}
            - 'records' : list like
              [{column -> value}, ... , {column -> value}]
            - 'index' : dict like {index -> {column -> value}}

            Abbreviations are allowed. `s` indicates `series` and `sp`
            indicates `split`.

            .. versionadded:: 1.4.0
                'tight' as an allowed value for the ``orient`` argument

        into : class, default dict
            The collections.abc.Mapping subclass used for all Mappings
            in the return value.  Can be the actual class or an empty
            instance of the mapping type you want.  If you want a
            collections.defaultdict, you must pass it initialized.

        Returns
        -------
        dict, list or collections.abc.Mapping
            Return a collections.abc.Mapping object representing the DataFrame.
            The resulting transformation depends on the `orient` parameter.

        See Also
        --------
        DataFrame.from_dict: Create a DataFrame from a dictionary.
        DataFrame.to_json: Convert a DataFrame to JSON format.

        Examples
        --------
        >>> df = pd.DataFrame({'col1': [1, 2],
        ...                    'col2': [0.5, 0.75]},
        ...                   index=['row1', 'row2'])
        >>> df
              col1  col2
        row1     1  0.50
        row2     2  0.75
        >>> df.to_dict()
        {'col1': {'row1': 1, 'row2': 2}, 'col2': {'row1': 0.5, 'row2': 0.75}}

        You can specify the return orientation.

        >>> df.to_dict('series')
        {'col1': row1    1
                 row2    2
        Name: col1, dtype: int64,
        'col2': row1    0.50
                row2    0.75
        Name: col2, dtype: float64}

        >>> df.to_dict('split')
        {'index': ['row1', 'row2'], 'columns': ['col1', 'col2'],
         'data': [[1, 0.5], [2, 0.75]]}

        >>> df.to_dict('records')
        [{'col1': 1, 'col2': 0.5}, {'col1': 2, 'col2': 0.75}]

        >>> df.to_dict('index')
        {'row1': {'col1': 1, 'col2': 0.5}, 'row2': {'col1': 2, 'col2': 0.75}}

        >>> df.to_dict('tight')
        {'index': ['row1', 'row2'], 'columns': ['col1', 'col2'],
         'data': [[1, 0.5], [2, 0.75]], 'index_names': [None], 'column_names': [None]}

        You can also specify the mapping type.

        >>> from collections import OrderedDict, defaultdict
        >>> df.to_dict(into=OrderedDict)
        OrderedDict([('col1', OrderedDict([('row1', 1), ('row2', 2)])),
                     ('col2', OrderedDict([('row1', 0.5), ('row2', 0.75)]))])

        If you want a `defaultdict`, you need to initialize it:

        >>> dd = defaultdict(list)
        >>> df.to_dict('records', into=dd)
        [defaultdict(<class 'list'>, {'col1': 1, 'col2': 0.5}),
         defaultdict(<class 'list'>, {'col1': 2, 'col2': 0.75})]
        """
        if not self.columns.is_unique:
            warnings.warn(
                "DataFrame columns are not unique, some columns will be omitted.",
                UserWarning,
                stacklevel=find_stack_level(),
            )
        # GH16122
        into_c = com.standardize_mapping(into)

        orient = orient.lower()
        # GH32515
        if orient.startswith(("d", "l", "s", "r", "i")) and orient not in {
            "dict",
            "list",
            "series",
            "split",
            "records",
            "index",
        }:
            warnings.warn(
                "Using short name for 'orient' is deprecated. Only the "
                "options: ('dict', list, 'series', 'split', 'records', 'index') "
                "will be used in a future version. Use one of the above "
                "to silence this warning.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

            if orient.startswith("d"):
                orient = "dict"
            elif orient.startswith("l"):
                orient = "list"
            elif orient.startswith("sp"):
                orient = "split"
            elif orient.startswith("s"):
                orient = "series"
            elif orient.startswith("r"):
                orient = "records"
            elif orient.startswith("i"):
                orient = "index"

        if orient == "dict":
            return into_c((k, v.to_dict(into)) for k, v in self.items())

        elif orient == "list":
            return into_c((k, v.tolist()) for k, v in self.items())

        elif orient == "split":
            return into_c(
                (
                    ("index", self.index.tolist()),
                    ("columns", self.columns.tolist()),
                    (
                        "data",
                        [
                            list(map(maybe_box_native, t))
                            for t in self.itertuples(index=False, name=None)
                        ],
                    ),
                )
            )

        elif orient == "tight":
            return into_c(
                (
                    ("index", self.index.tolist()),
                    ("columns", self.columns.tolist()),
                    (
                        "data",
                        [
                            list(map(maybe_box_native, t))
                            for t in self.itertuples(index=False, name=None)
                        ],
                    ),
                    ("index_names", list(self.index.names)),
                    ("column_names", list(self.columns.names)),
                )
            )

        elif orient == "series":
            return into_c((k, v) for k, v in self.items())

        elif orient == "records":
            columns = self.columns.tolist()
            rows = (
                dict(zip(columns, row))
                for row in self.itertuples(index=False, name=None)
            )
            return [
                into_c((k, maybe_box_native(v)) for k, v in row.items()) for row in rows
            ]

        elif orient == "index":
            if not self.index.is_unique:
                raise ValueError("DataFrame index must be unique for orient='index'.")
            return into_c(
                (t[0], dict(zip(self.columns, t[1:])))
                for t in self.itertuples(name=None)
            )

        else:
            raise ValueError(f"orient '{orient}' not understood")
