    def __getitem__(self, key):
        if is_scalar(key):
            retval = []
            for lev, lab in zip(self.levels, self.labels):
                if lab[key] == -1:
                    retval.append(np.nan)
                else:
                    retval.append(lev[lab[key]])

            return tuple(retval)
        else:
            if com.is_bool_indexer(key):
                key = np.asarray(key)
                sortorder = self.sortorder
            else:
                # cannot be sure whether the result will be sorted
                sortorder = None

                if isinstance(key, Index):
                    key = np.asarray(key)

            new_labels = [lab[key] for lab in self.labels]

            return MultiIndex(levels=self.levels, labels=new_labels,
                              names=self.names, sortorder=sortorder,
                              verify_integrity=False)
