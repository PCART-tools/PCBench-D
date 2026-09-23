    def itertuples(self, index=True, name="Pandas"):
        """
        Iterate over DataFrame rows as namedtuples.

        Parameters
        ----------
        index : bool, default True
            If True, return the index as the first element of the tuple.
        name : str, default "Pandas"
            The name of the returned namedtuples or None to return regular
            tuples.

        Yields
        -------
        collections.namedtuple
            Yields a namedtuple for each row in the DataFrame with the first
            field possibly being the index and following fields being the
            column values.

        See Also
        --------
        DataFrame.iterrows : Iterate over DataFrame rows as (index, Series)
            pairs.
        DataFrame.iteritems : Iterate over (column name, Series) pairs.

        Notes
        -----
        The column names will be renamed to positional names if they are
        invalid Python identifiers, repeated, or start with an underscore.
        With a large number of columns (>255), regular tuples are returned.

        Examples
        --------
        >>> df = pd.DataFrame({'num_legs': [4, 2], 'num_wings': [0, 2]},
        ...                   index=['dog', 'hawk'])
        >>> df
              num_legs  num_wings
        dog          4          0
        hawk         2          2
        >>> for row in df.itertuples():
        ...     print(row)
        ...
        Pandas(Index='dog', num_legs=4, num_wings=0)
        Pandas(Index='hawk', num_legs=2, num_wings=2)

        By setting the `index` parameter to False we can remove the index
        as the first element of the tuple:

        >>> for row in df.itertuples(index=False):
        ...     print(row)
        ...
        Pandas(num_legs=4, num_wings=0)
        Pandas(num_legs=2, num_wings=2)

        With the `name` parameter set we set a custom name for the yielded
        namedtuples:

        >>> for row in df.itertuples(name='Animal'):
        ...     print(row)
        ...
        Animal(Index='dog', num_legs=4, num_wings=0)
        Animal(Index='hawk', num_legs=2, num_wings=2)
        """
        arrays = []
        fields = list(self.columns)
        if index:
            arrays.append(self.index)
            fields.insert(0, "Index")

        # use integer indexing because of possible duplicate column names
        arrays.extend(self.iloc[:, k] for k in range(len(self.columns)))

        # Python 3 supports at most 255 arguments to constructor, and
        # things get slow with this many fields in Python 2
        if name is not None and len(self.columns) + index < 256:
            # `rename` is unsupported in Python 2.6
            try:
                itertuple = collections.namedtuple(name, fields, rename=True)
                return map(itertuple._make, zip(*arrays))

            except Exception:
                pass

        # fallback to regular tuples
        return zip(*arrays)
