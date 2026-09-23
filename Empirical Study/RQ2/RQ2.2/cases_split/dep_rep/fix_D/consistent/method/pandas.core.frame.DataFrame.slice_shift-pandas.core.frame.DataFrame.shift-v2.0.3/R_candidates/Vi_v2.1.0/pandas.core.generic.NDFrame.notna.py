    @doc(klass=_shared_doc_kwargs["klass"])
    def notna(self) -> Self:
        """
        Detect existing (non-missing) values.

        Return a boolean same-sized object indicating if the values are not NA.
        Non-missing values get mapped to True. Characters such as empty
        strings ``''`` or :attr:`numpy.inf` are not considered NA values
        (unless you set ``pandas.options.mode.use_inf_as_na = True``).
        NA values, such as None or :attr:`numpy.NaN`, get mapped to False
        values.

        Returns
        -------
        {klass}
            Mask of bool values for each element in {klass} that
            indicates whether an element is not an NA value.

        See Also
        --------
        {klass}.notnull : Alias of notna.
        {klass}.isna : Boolean inverse of notna.
        {klass}.dropna : Omit axes labels with missing values.
        notna : Top-level notna.

        Examples
        --------
        Show which entries in a DataFrame are not NA.

        >>> df = pd.DataFrame(dict(age=[5, 6, np.nan],
        ...                        born=[pd.NaT, pd.Timestamp('1939-05-27'),
        ...                              pd.Timestamp('1940-04-25')],
        ...                        name=['Alfred', 'Batman', ''],
        ...                        toy=[None, 'Batmobile', 'Joker']))
        >>> df
           age       born    name        toy
        0  5.0        NaT  Alfred       None
        1  6.0 1939-05-27  Batman  Batmobile
        2  NaN 1940-04-25              Joker

        >>> df.notna()
             age   born  name    toy
        0   True  False  True  False
        1   True   True  True   True
        2  False   True  True   True

        Show which entries in a Series are not NA.

        >>> ser = pd.Series([5, 6, np.nan])
        >>> ser
        0    5.0
        1    6.0
        2    NaN
        dtype: float64

        >>> ser.notna()
        0     True
        1     True
        2    False
        dtype: bool
        """
        return notna(self).__finalize__(self, method="notna")
