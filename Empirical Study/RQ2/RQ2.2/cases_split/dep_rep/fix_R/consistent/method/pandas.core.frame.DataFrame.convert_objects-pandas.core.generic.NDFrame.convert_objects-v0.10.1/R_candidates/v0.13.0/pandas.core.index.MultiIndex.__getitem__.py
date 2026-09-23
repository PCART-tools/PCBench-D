    def __getitem__(self, key):
        if np.isscalar(key):
            retval = []
            for lev, lab in zip(self.levels, self.labels):
                if lab[key] == -1:
                    retval.append(np.nan)
                else:
                    retval.append(lev[lab[key]])

            return tuple(retval)
        else:
            if com._is_bool_indexer(key):
                key = np.asarray(key)
                sortorder = self.sortorder
            else:
                # cannot be sure whether the result will be sorted
                sortorder = None

            result = np.empty(0, dtype=object).view(type(self))
            new_labels = [lab[key] for lab in self.labels]

            # an optimization
            result._set_levels(self.levels, validate=False)
            result._set_labels(new_labels)
            result.sortorder = sortorder
            result._set_names(self.names)

            return result
