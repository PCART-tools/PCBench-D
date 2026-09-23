    def to_dict(self, orient='dict', into=dict):
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
            - 'records' : list like
              [{column -> value}, ... , {column -> value}]
            - 'index' : dict like {index -> {column -> value}}

            Abbreviations are allowed. `s` indicates `series` and `sp`
            indicates `split`.

        into : class, default dict
            The collections.Mapping subclass used for all Mappings
            in the return value.  Can be the actual class or an empty
            instance of the mapping type you want.  If you want a
            collections.defaultdict, you must pass it initialized.

            .. versionadded:: 0.21.0

        Returns
        -------
        result : collections.Mapping like {column -> {index -> value}}

        See Also
        --------
        DataFrame.from_dict: create a DataFrame from a dictionary
        DataFrame.to_json: convert a DataFrame to JSON format

        Examples
        --------
        >>> df = pd.DataFrame({'col1': [1, 2],
        ...                    'col2': [0.5, 0.75]},
        ...                   index=['a', 'b'])
        >>> df
           col1  col2
        a     1   0.50
        b     2   0.75
        >>> df.to_dict()
        {'col1': {'a': 1, 'b': 2}, 'col2': {'a': 0.5, 'b': 0.75}}

        You can specify the return orientation.

        >>> df.to_dict('series')
        {'col1': a    1
                 b    2
                 Name: col1, dtype: int64,
         'col2': a    0.50
                 b    0.75
                 Name: col2, dtype: float64}

        >>> df.to_dict('split')
        {'index': ['a', 'b'], 'columns': ['col1', 'col2'],
         'data': [[1.0, 0.5], [2.0, 0.75]]}

        >>> df.to_dict('records')
        [{'col1': 1.0, 'col2': 0.5}, {'col1': 2.0, 'col2': 0.75}]

        >>> df.to_dict('index')
        {'a': {'col1': 1.0, 'col2': 0.5}, 'b': {'col1': 2.0, 'col2': 0.75}}

        You can also specify the mapping type.

        >>> from collections import OrderedDict, defaultdict
        >>> df.to_dict(into=OrderedDict)
        OrderedDict([('col1', OrderedDict([('a', 1), ('b', 2)])),
                     ('col2', OrderedDict([('a', 0.5), ('b', 0.75)]))])

        If you want a `defaultdict`, you need to initialize it:

        >>> dd = defaultdict(list)
        >>> df.to_dict('records', into=dd)
        [defaultdict(<class 'list'>, {'col1': 1.0, 'col2': 0.5}),
         defaultdict(<class 'list'>, {'col1': 2.0, 'col2': 0.75})]
        """
        if not self.columns.is_unique:
            warnings.warn("DataFrame columns are not unique, some "
                          "columns will be omitted.", UserWarning,
                          stacklevel=2)
        # GH16122
        into_c = com.standardize_mapping(into)
        if orient.lower().startswith('d'):
            return into_c(
                (k, v.to_dict(into)) for k, v in compat.iteritems(self))
        elif orient.lower().startswith('l'):
            return into_c((k, v.tolist()) for k, v in compat.iteritems(self))
        elif orient.lower().startswith('sp'):
            return into_c((('index', self.index.tolist()),
                           ('columns', self.columns.tolist()),
                           ('data', lib.map_infer(self.values.ravel(),
                                                  com._maybe_box_datetimelike)
                            .reshape(self.values.shape).tolist())))
        elif orient.lower().startswith('s'):
            return into_c((k, com._maybe_box_datetimelike(v))
                          for k, v in compat.iteritems(self))
        elif orient.lower().startswith('r'):
            return [into_c((k, com._maybe_box_datetimelike(v))
                           for k, v in zip(self.columns, np.atleast_1d(row)))
                    for row in self.values]
        elif orient.lower().startswith('i'):
            return into_c((t[0], dict(zip(self.columns, t[1:])))
                          for t in self.itertuples())
        else:
            raise ValueError("orient '{o}' not understood".format(o=orient))
