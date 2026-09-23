    def __setitem__(self, key, value):
        """ Item assignment.


        Raises
        ------
        ValueError
            If (one or more) Value is not in categories or if a assigned
            `Categorical` does not have the same categories
        """

        # require identical categories set
        if isinstance(value, Categorical):
            if not value.categories.equals(self.categories):
                raise ValueError("Cannot set a Categorical with another, "
                                 "without identical categories")

        rvalue = value if is_list_like(value) else [value]

        from pandas import Index
        to_add = Index(rvalue).difference(self.categories)

        # no assignments of values not in categories, but it's always ok to set
        # something to np.nan
        if len(to_add) and not isna(to_add).all():
            raise ValueError("Cannot setitem on a Categorical with a new "
                             "category, set the categories first")

        # set by position
        if isinstance(key, (int, np.integer)):
            pass

        # tuple of indexers (dataframe)
        elif isinstance(key, tuple):
            # only allow 1 dimensional slicing, but can
            # in a 2-d case be passd (slice(None),....)
            if len(key) == 2:
                if not is_null_slice(key[0]):
                    raise AssertionError("invalid slicing for a 1-ndim "
                                         "categorical")
                key = key[1]
            elif len(key) == 1:
                key = key[0]
            else:
                raise AssertionError("invalid slicing for a 1-ndim "
                                     "categorical")

        # slicing in Series or Categorical
        elif isinstance(key, slice):
            pass

        # Array of True/False in Series or Categorical
        else:
            # There is a bug in numpy, which does not accept a Series as a
            # indexer
            # https://github.com/pandas-dev/pandas/issues/6168
            # https://github.com/numpy/numpy/issues/4240 -> fixed in numpy 1.9
            # FIXME: remove when numpy 1.9 is the lowest numpy version pandas
            # accepts...
            key = np.asarray(key)

        lindexer = self.categories.get_indexer(rvalue)

        # FIXME: the following can be removed after GH7820 is fixed:
        # https://github.com/pandas-dev/pandas/issues/7820
        # float categories do currently return -1 for np.nan, even if np.nan is
        # included in the index -> "repair" this here
        if isna(rvalue).any() and isna(self.categories).any():
            nan_pos = np.where(isna(self.categories))[0]
            lindexer[lindexer == -1] = nan_pos

        lindexer = self._maybe_coerce_indexer(lindexer)
        self._codes[key] = lindexer
