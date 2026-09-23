    @classmethod
    def from_items(cls, items, columns=None, orient='columns'):
        """
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
        frame : DataFrame
        """
        keys, values = lzip(*items)

        if orient == 'columns':
            if columns is not None:
                columns = _ensure_index(columns)

                idict = dict(items)
                if len(idict) < len(items):
                    if not columns.equals(_ensure_index(keys)):
                        raise ValueError('With non-unique item names, passed '
                                         'columns must be identical')
                    arrays = values
                else:
                    arrays = [idict[k] for k in columns if k in idict]
            else:
                columns = _ensure_index(keys)
                arrays = values

            return cls._from_arrays(arrays, columns, None)
        elif orient == 'index':
            if columns is None:
                raise TypeError("Must pass columns with orient='index'")

            keys = _ensure_index(keys)

            arr = np.array(values, dtype=object).T
            data = [lib.maybe_convert_objects(v) for v in arr]
            return cls._from_arrays(data, columns, keys)
        else:  # pragma: no cover
            raise ValueError("'orient' must be either 'columns' or 'index'")
