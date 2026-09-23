    def to_dataframe(self, columns=None):
        """ Create Dask Dataframe from a Dask Bag

        Bag should contain tuples, dict records, or scalars.

        Index will not be particularly meaningful.  Use ``reindex`` afterwards
        if necessary.

        Parameters
        ----------
        columns : pandas.DataFrame or list, optional
            If a ``pandas.DataFrame``, it should mirror the column names and
            dtypes of the output dataframe. If a list, it provides the desired
            column names. If not provided or a list, a single element from
            the first partition will be computed, triggering a potentially
            expensive call to ``compute``. Providing a list is only useful for
            selecting subset of columns, to avoid an internal compute call you
            must provide a ``pandas.DataFrame`` as dask requires dtype knowledge
            ahead of time.

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
        if isinstance(columns, pd.DataFrame):
            meta = columns
        else:
            head = self.take(1)[0]
            meta = pd.DataFrame([head], columns=columns)
        # Serializing the columns and dtypes is much smaller than serializing
        # the empty frame
        cols = list(meta.columns)
        dtypes = meta.dtypes.to_dict()
        name = 'to_dataframe-' + tokenize(self, cols, dtypes)
        dsk = {(name, i): (to_dataframe, (list2, (self.name, i)), cols, dtypes)
               for i in range(self.npartitions)}

        divisions = [None] * (self.npartitions + 1)
        return dd.DataFrame(merge(optimize(self.dask, self._keys()), dsk),
                            name, meta, divisions)
