class StringAccessor(Accessor):
    """ Accessor object for string properties of the Series values.

    Examples
    --------

    >>> s.str.lower()  # doctest: +SKIP
    """
    _accessor = pd.Series.str
    _accessor_name = 'str'
    _not_implemented = {'get_dummies'}

    def _validate(self, series):
        if not (series.dtype == 'object' or (
                is_categorical_dtype(series) and
                series.cat.categories.dtype == 'object')):
            raise AttributeError("Can only use .str accessor with object dtype")

    @derived_from(pd.core.strings.StringMethods)
    def split(self, pat=None, n=-1):
        return self._function_map('split', pat=pat, n=n)

    @derived_from(pd.core.strings.StringMethods)
    def cat(self, others=None, sep=None, na_rep=None):
        from .core import Series, Index
        if others is None:
            raise NotImplementedError("x.str.cat() with `others == None`")

        valid_types = (Series, Index, pd.Series, pd.Index)
        if isinstance(others, valid_types):
            others = [others]
        elif not all(isinstance(a, valid_types) for a in others):
            raise TypeError("others must be Series/Index")

        return self._series.map_partitions(str_cat, *others, sep=sep,
                                           na_rep=na_rep, meta=self._series._meta)

    @derived_from(pd.core.strings.StringMethods)
    def extractall(self, pat, flags=0):
        # TODO: metadata inference here won't be necessary for pandas >= 0.23.0
        meta = self._series._meta.str.extractall(pat, flags=flags)
        if PANDAS_VERSION < '0.23.0':
            index_name = self._series.index.name
            meta.index = pd.MultiIndex(levels=[[], []],
                                       labels=[[], []],
                                       names=[index_name, 'match'])
        return self._series.map_partitions(str_extractall, pat, flags,
                                           meta=meta, token='str-extractall')

    def __getitem__(self, index):
        return self._series.map_partitions(str_get, index,
                                           meta=self._series._meta)
