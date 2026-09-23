    def itertuples(self, index=True, name="Pandas"):
        """
        Iterate over DataFrame rows as namedtuples, with index value as first
        element of the tuple.

        Parameters
        ----------
        index : boolean, default True
            If True, return the index as the first element of the tuple.
        name : string, default "Pandas"
            The name of the returned namedtuples or None to return regular
            tuples.

        Notes
        -----
        The column names will be renamed to positional names if they are
        invalid Python identifiers, repeated, or start with an underscore.
        With a large number of columns (>255), regular tuples are returned.

        See also
        --------
        iterrows : Iterate over DataFrame rows as (index, Series) pairs.
        iteritems : Iterate over (column name, Series) pairs.

        Examples
        --------

        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': [0.1, 0.2]},
                              index=['a', 'b'])
        >>> df
           col1  col2
        a     1   0.1
        b     2   0.2
        >>> for row in df.itertuples():
        ...     print(row)
        ...
        Pandas(Index='a', col1=1, col2=0.10000000000000001)
        Pandas(Index='b', col1=2, col2=0.20000000000000001)

        """
        arrays = []
        fields = []
        if index:
            arrays.append(self.index)
            fields.append("Index")

        # use integer indexing because of possible duplicate column names
        arrays.extend(self.iloc[:, k] for k in range(len(self.columns)))

        # Python 3 supports at most 255 arguments to constructor, and
        # things get slow with this many fields in Python 2
        if name is not None and len(self.columns) + index < 256:
            # `rename` is unsupported in Python 2.6
            try:
                itertuple = collections.namedtuple(name,
                                                   fields + list(self.columns),
                                                   rename=True)
                return map(itertuple._make, zip(*arrays))
            except Exception:
                pass

        # fallback to regular tuples
        return zip(*arrays)
