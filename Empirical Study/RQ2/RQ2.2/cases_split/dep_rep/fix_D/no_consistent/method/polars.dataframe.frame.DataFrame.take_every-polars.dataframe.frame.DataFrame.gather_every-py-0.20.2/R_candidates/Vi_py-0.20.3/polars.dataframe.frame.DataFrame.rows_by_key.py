    def rows_by_key(
        self,
        key: ColumnNameOrSelector | Sequence[ColumnNameOrSelector],
        *,
        named: bool = False,
        include_key: bool = False,
        unique: bool = False,
    ) -> dict[Any, Iterable[Any]]:
        """
        Returns DataFrame data as a keyed dictionary of python-native values.

        Note that this method should not be used in place of native operations, due to
        the high cost of materialising all frame data out into a dictionary; it should
        be used only when you need to move the values out into a Python data structure
        or other object that cannot operate directly with Polars/Arrow.

        Parameters
        ----------
        key
            The column(s) to use as the key for the returned dictionary. If multiple
            columns are specified, the key will be a tuple of those values, otherwise
            it will be a string.
        named
            Return dictionary rows instead of tuples, mapping column name to row value.
        include_key
            Include key values inline with the associated data (by default the key
            values are omitted as a memory/performance optimisation, as they can be
            reoconstructed from the key).
        unique
            Indicate that the key is unique; this will result in a 1:1 mapping from
            key to a single associated row. Note that if the key is *not* actually
            unique the last row with the given key will be returned.

        Notes
        -----
        If you have `ns`-precision temporal values you should be aware that Python
        natively only supports up to `μs`-precision; `ns`-precision values will be
        truncated to microseconds on conversion to Python. If this matters to your
        use-case you should export to a different format (such as Arrow or NumPy).

        See Also
        --------
        rows : Materialise all frame data as a list of rows (potentially expensive).
        iter_rows : Row iterator over frame data (does not materialise all rows).

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "w": ["a", "b", "b", "a"],
        ...         "x": ["q", "q", "q", "k"],
        ...         "y": [1.0, 2.5, 3.0, 4.5],
        ...         "z": [9, 8, 7, 6],
        ...     }
        ... )

        Group rows by the given key column(s):

        >>> df.rows_by_key(key=["w"])
        defaultdict(<class 'list'>,
            {'a': [('q', 1.0, 9), ('k', 4.5, 6)],
             'b': [('q', 2.5, 8), ('q', 3.0, 7)]})

        Return the same row groupings as dictionaries:

        >>> df.rows_by_key(key=["w"], named=True)
        defaultdict(<class 'list'>,
            {'a': [{'x': 'q', 'y': 1.0, 'z': 9},
                   {'x': 'k', 'y': 4.5, 'z': 6}],
             'b': [{'x': 'q', 'y': 2.5, 'z': 8},
                   {'x': 'q', 'y': 3.0, 'z': 7}]})

        Return row groupings, assuming keys are unique:

        >>> df.rows_by_key(key=["z"], unique=True)
        {9: ('a', 'q', 1.0),
         8: ('b', 'q', 2.5),
         7: ('b', 'q', 3.0),
         6: ('a', 'k', 4.5)}

        Return row groupings as dictionaries, assuming keys are unique:

        >>> df.rows_by_key(key=["z"], named=True, unique=True)
        {9: {'w': 'a', 'x': 'q', 'y': 1.0},
         8: {'w': 'b', 'x': 'q', 'y': 2.5},
         7: {'w': 'b', 'x': 'q', 'y': 3.0},
         6: {'w': 'a', 'x': 'k', 'y': 4.5}}

        Return dictionary rows grouped by a compound key, including key values:

        >>> df.rows_by_key(key=["w", "x"], named=True, include_key=True)
        defaultdict(<class 'list'>,
            {('a', 'q'): [{'w': 'a', 'x': 'q', 'y': 1.0, 'z': 9}],
             ('b', 'q'): [{'w': 'b', 'x': 'q', 'y': 2.5, 'z': 8},
                          {'w': 'b', 'x': 'q', 'y': 3.0, 'z': 7}],
             ('a', 'k'): [{'w': 'a', 'x': 'k', 'y': 4.5, 'z': 6}]})

        """
        from polars.selectors import expand_selector, is_selector

        if is_selector(key):
            key_tuple = expand_selector(target=self, selector=key)
        elif not isinstance(key, str):
            key_tuple = tuple(key)  # type: ignore[arg-type]
        else:
            key_tuple = (key,)

        # establish index or name-based getters for the key and data values
        data_cols = [k for k in self.schema if k not in key_tuple]
        if named:
            get_data = itemgetter(*data_cols)
            get_key = itemgetter(*key_tuple)
        else:
            data_idxs, index_idxs = [], []
            for idx, c in enumerate(self.columns):
                if c in key_tuple:
                    index_idxs.append(idx)
                else:
                    data_idxs.append(idx)
            if not index_idxs:
                raise ValueError(f"no columns found for key: {key_tuple!r}")
            get_data = itemgetter(*data_idxs)  # type: ignore[assignment]
            get_key = itemgetter(*index_idxs)  # type: ignore[assignment]

        # if unique, we expect to write just one entry per key; otherwise, we're
        # returning a list of rows for each key, so append into a defaultdict.
        rows: dict[Any, Any] = {} if unique else defaultdict(list)

        # return named values (key -> dict | list of dicts), eg:
        # "{(key,): [{col:val, col:val, ...}],
        #   (key,): [{col:val, col:val, ...}],}"
        if named:
            if unique and include_key:
                rows = {get_key(row): row for row in self.iter_rows(named=True)}
            else:
                for d in self.iter_rows(named=True):
                    k = get_key(d)
                    if not include_key:
                        for ix in key_tuple:
                            del d[ix]  # type: ignore[arg-type]
                    if unique:
                        rows[k] = d
                    else:
                        rows[k].append(d)

        # return values (key -> tuple | list of tuples), eg:
        # "{(key,): [(val, val, ...)],
        #   (key,): [(val, val, ...)], ...}"
        elif unique:
            rows = (
                {get_key(row): row for row in self.iter_rows()}
                if include_key
                else {get_key(row): get_data(row) for row in self.iter_rows()}
            )
        elif include_key:
            for row in self.iter_rows(named=False):
                rows[get_key(row)].append(row)
        else:
            for row in self.iter_rows(named=False):
                rows[get_key(row)].append(get_data(row))

        return rows
