    def _str_get_dummies(self, sep="|"):
        from pandas import Series

        arr = Series(self).fillna("")
        try:
            arr = sep + arr + sep
        except (TypeError, NotImplementedError):
            arr = sep + arr.astype(str) + sep

        tags: set[str] = set()
        for ts in Series(arr).str.split(sep):
            tags.update(ts)
        tags2 = sorted(tags - {""})

        dummies = np.empty((len(arr), len(tags2)), dtype=np.int64)

        for i, t in enumerate(tags2):
            pat = sep + t + sep
            dummies[:, i] = lib.map_infer(arr.to_numpy(), lambda x: pat in x)
        return dummies, tags2
