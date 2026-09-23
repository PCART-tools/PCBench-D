    def _iset_not_inplace(self, key, value):
        # GH#39510 when setting with df[key] = obj with a list-like key and
        #  list-like value, we iterate over those listlikes and set columns
        #  one at a time.  This is different from dispatching to
        #  `self.loc[:, key]= value`  because loc.__setitem__ may overwrite
        #  data inplace, whereas this will insert new arrays.

        def igetitem(obj, i: int):
            # Note: we catch DataFrame obj before getting here, but
            #  hypothetically would return obj.iloc[:, i]
            if isinstance(obj, np.ndarray):
                return obj[..., i]
            else:
                return obj[i]

        if self.columns.is_unique:
            if np.shape(value)[-1] != len(key):
                raise ValueError("Columns must be same length as key")

            for i, col in enumerate(key):
                self[col] = igetitem(value, i)

        else:
            ilocs = self.columns.get_indexer_non_unique(key)[0]
            if (ilocs < 0).any():
                # key entries not in self.columns
                raise NotImplementedError

            if np.shape(value)[-1] != len(ilocs):
                raise ValueError("Columns must be same length as key")

            assert np.ndim(value) <= 2

            orig_columns = self.columns

            # Using self.iloc[:, i] = ... may set values inplace, which
            #  by convention we do not do in __setitem__
            try:
                self.columns = Index(range(len(self.columns)))
                for i, iloc in enumerate(ilocs):
                    self[iloc] = igetitem(value, i)
            finally:
                self.columns = orig_columns
