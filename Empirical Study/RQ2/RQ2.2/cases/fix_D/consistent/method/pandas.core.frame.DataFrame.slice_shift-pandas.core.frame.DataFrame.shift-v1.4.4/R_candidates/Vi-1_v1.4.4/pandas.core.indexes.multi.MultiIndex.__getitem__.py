    def __getitem__(self, key):
        if is_scalar(key):
            key = com.cast_scalar_indexer(key, warn_float=True)

            retval = []
            for lev, level_codes in zip(self.levels, self.codes):
                if level_codes[key] == -1:
                    retval.append(np.nan)
                else:
                    retval.append(lev[level_codes[key]])

            return tuple(retval)
        else:
            # in general cannot be sure whether the result will be sorted
            sortorder = None
            if com.is_bool_indexer(key):
                key = np.asarray(key, dtype=bool)
                sortorder = self.sortorder
            elif isinstance(key, slice):
                if key.step is None or key.step > 0:
                    sortorder = self.sortorder
            elif isinstance(key, Index):
                key = np.asarray(key)

            new_codes = [level_codes[key] for level_codes in self.codes]

            return MultiIndex(
                levels=self.levels,
                codes=new_codes,
                names=self.names,
                sortorder=sortorder,
                verify_integrity=False,
            )
