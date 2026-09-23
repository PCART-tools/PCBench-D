    @classmethod
    def from_items(cls, items, columns=None, orient="columns"):
        """
        Construct a DataFrame from a list of tuples.

        .. deprecated:: 0.23.0
          `from_items` is deprecated and will be removed in a future version.
          Use :meth:`DataFrame.from_dict(dict(items)) <DataFrame.from_dict>`
          instead.
          :meth:`DataFrame.from_dict(OrderedDict(items)) <DataFrame.from_dict>`
          may be used to preserve the key order.

        Convert (key, value) pairs to DataFrame. The keys will be the axis
        index (usually the columns, but depends on the specified
        orientation). The values should be arrays or Series.

        Parameters
        ----------
        items : sequence of (key, value) pairs
            Values should be arrays or Series.
        columns : sequence of column labels, optional
            Must be passed if orient='index'.
        orient : {'columns', 'index'}, default 'columns'
            The "orientation" of the data. If the keys of the
            input correspond to column labels, pass 'columns'
            (default). Otherwise if the keys correspond to the index,
            pass 'index'.

        Returns
        -------
        DataFrame
        """

        warnings.warn(
            "from_items is deprecated. Please use "
            "DataFrame.from_dict(dict(items), ...) instead. "
            "DataFrame.from_dict(OrderedDict(items)) may be used to "
            "preserve the key order.",
            FutureWarning,
            stacklevel=2,
        )

        keys, values = zip(*items)

        if orient == "columns":
            if columns is not None:
                columns = ensure_index(columns)

                idict = dict(items)
                if len(idict) < len(items):
                    if not columns.equals(ensure_index(keys)):
                        raise ValueError(
                            "With non-unique item names, passed "
                            "columns must be identical"
                        )
                    arrays = values
                else:
                    arrays = [idict[k] for k in columns if k in idict]
            else:
                columns = ensure_index(keys)
                arrays = values

            # GH 17312
            # Provide more informative error msg when scalar values passed
            try:
                return cls._from_arrays(arrays, columns, None)

            except ValueError:
                if not is_nested_list_like(values):
                    raise ValueError(
                        "The value in each (key, value) pair "
                        "must be an array, Series, or dict"
                    )

        elif orient == "index":
            if columns is None:
                raise TypeError("Must pass columns with orient='index'")

            keys = ensure_index(keys)

            # GH 17312
            # Provide more informative error msg when scalar values passed
            try:
                arr = np.array(values, dtype=object).T
                data = [lib.maybe_convert_objects(v) for v in arr]
                return cls._from_arrays(data, columns, keys)

            except TypeError:
                if not is_nested_list_like(values):
                    raise ValueError(
                        "The value in each (key, value) pair "
                        "must be an array, Series, or dict"
                    )

        else:  # pragma: no cover
            raise ValueError("'orient' must be either 'columns' or 'index'")
