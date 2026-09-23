    def join(self, other, on=None, how='left', lsuffix='', rsuffix='',
             sort=False):
        """
        Join columns with other DataFrame either on index or on a key
        column. Efficiently Join multiple DataFrame objects by index at once by
        passing a list.

        Parameters
        ----------
        other : DataFrame, Series with name field set, or list of DataFrame
            Index should be similar to one of the columns in this one. If a
            Series is passed, its name attribute must be set, and that will be
            used as the column name in the resulting joined DataFrame
        on : column name, tuple/list of column names, or array-like
            Column(s) in the caller to join on the index in other,
            otherwise joins index-on-index. If multiples
            columns given, the passed DataFrame must have a MultiIndex. Can
            pass an array as the join key if not already contained in the
            calling DataFrame. Like an Excel VLOOKUP operation
        how : {'left', 'right', 'outer', 'inner'}, default: 'left'
            How to handle the operation of the two objects.

            * left: use calling frame's index (or column if on is specified)
            * right: use other frame's index
            * outer: form union of calling frame's index (or column if on is
                specified) with other frame's index
            * inner: form intersection of calling frame's index (or column if
                on is specified) with other frame's index
        lsuffix : string
            Suffix to use from left frame's overlapping columns
        rsuffix : string
            Suffix to use from right frame's overlapping columns
        sort : boolean, default False
            Order result DataFrame lexicographically by the join key. If False,
            preserves the index order of the calling (left) DataFrame

        Notes
        -----
        on, lsuffix, and rsuffix options are not supported when passing a list
        of DataFrame objects

        Examples
        --------
        >>> caller = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3', 'K4', 'K5'],
        ...                        'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})

        >>> caller
            A key
        0  A0  K0
        1  A1  K1
        2  A2  K2
        3  A3  K3
        4  A4  K4
        5  A5  K5

        >>> other = pd.DataFrame({'key': ['K0', 'K1', 'K2'],
        ...                       'B': ['B0', 'B1', 'B2']})

        >>> other
            B key
        0  B0  K0
        1  B1  K1
        2  B2  K2

        Join DataFrames using their indexes.

        >>> caller.join(other, lsuffix='_caller', rsuffix='_other')

        >>>     A key_caller    B key_other
            0  A0         K0   B0        K0
            1  A1         K1   B1        K1
            2  A2         K2   B2        K2
            3  A3         K3  NaN       NaN
            4  A4         K4  NaN       NaN
            5  A5         K5  NaN       NaN


        If we want to join using the key columns, we need to set key to be
        the index in both caller and other. The joined DataFrame will have
        key as its index.

        >>> caller.set_index('key').join(other.set_index('key'))

        >>>      A    B
            key
            K0   A0   B0
            K1   A1   B1
            K2   A2   B2
            K3   A3  NaN
            K4   A4  NaN
            K5   A5  NaN

        Another option to join using the key columns is to use the on
        parameter. DataFrame.join always uses other's index but we can use any
        column in the caller. This method preserves the original caller's
        index in the result.

        >>> caller.join(other.set_index('key'), on='key')

        >>>     A key    B
            0  A0  K0   B0
            1  A1  K1   B1
            2  A2  K2   B2
            3  A3  K3  NaN
            4  A4  K4  NaN
            5  A5  K5  NaN


        See also
        --------
        DataFrame.merge : For column(s)-on-columns(s) operations

        Returns
        -------
        joined : DataFrame
        """
        # For SparseDataFrame's benefit
        return self._join_compat(other, on=on, how=how, lsuffix=lsuffix,
                                 rsuffix=rsuffix, sort=sort)
