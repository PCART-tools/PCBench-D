    def to_dataframe(self, meta=None, columns=None):
        """ Create Dask Dataframe from a Dask Bag

        Bag should contain tuples, dict records, or scalars.

        Index will not be particularly meaningful.  Use ``reindex`` afterwards
        if necessary.

        Parameters
        ----------
        meta : pd.DataFrame, dict, iterable, optional
            An empty ``pd.DataFrame`` that matches the dtypes and column names
            of the output. This metadata is necessary for many algorithms in
            dask dataframe to work.  For ease of use, some alternative inputs
            are also available. Instead of a ``DataFrame``, a ``dict`` of
            ``{name: dtype}`` or iterable of ``(name, dtype)`` can be provided.
            If not provided or a list, a single element from the first
            partition will be computed, triggering a potentially expensive call
            to ``compute``. This may lead to unexpected results, so providing
            ``meta`` is recommended. For more information, see
            ``dask.dataframe.utils.make_meta``.
        columns : sequence, optional
            Column names to use. If the passed data do not have names
            associated with them, this argument provides names for the columns.
            Otherwise this argument indicates the order of the columns in the
            result (any names not found in the data will become all-NA
            columns).  Note that if ``meta`` is provided, column names will be
            taken from there and this parameter is invalid.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence([{'name': 'Alice',   'balance': 100},
        ...                       {'name': 'Bob',     'balance': 200},
        ...                       {'name': 'Charlie', 'balance': 300}],
        ...                      npartitions=2)
        >>> df = b.to_dataframe()

        >>> df.compute()
           balance     name
        0      100    Alice
        1      200      Bob
        0      300  Charlie
        """
        import pandas as pd
        import dask.dataframe as dd
        if meta is None:
            if isinstance(columns, pd.DataFrame):
                warn("Passing metadata to `columns` is deprecated. Please "
                     "use the `meta` keyword instead.")
                meta = columns
            else:
                head = self.take(1)[0]
                meta = pd.DataFrame([head], columns=columns)
        elif columns is not None:
            raise ValueError("Can't specify both `meta` and `columns`")
        else:
            meta = dd.utils.make_meta(meta)
        # Serializing the columns and dtypes is much smaller than serializing
        # the empty frame
        cols = list(meta.columns)
        dtypes = meta.dtypes.to_dict()
        name = 'to_dataframe-' + tokenize(self, cols, dtypes)
        dsk = {(name, i): (to_dataframe, (self.name, i), cols, dtypes)
               for i in range(self.npartitions)}

        divisions = [None] * (self.npartitions + 1)
        return dd.DataFrame(merge(optimize(self.dask, self._keys()), dsk),
                            name, meta, divisions)
