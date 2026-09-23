    def format(self, space=2, sparsify=None, adjoin=True, names=False,
               na_rep=None, formatter=None):
        if len(self) == 0:
            return []

        stringified_levels = []
        for lev, lab in zip(self.levels, self.labels):
            na = na_rep if na_rep is not None else _get_na_rep(lev.dtype.type)

            if len(lev) > 0:

                formatted = lev.take(lab).format(formatter=formatter)

                # we have some NA
                mask = lab == -1
                if mask.any():
                    formatted = np.array(formatted, dtype=object)
                    formatted[mask] = na
                    formatted = formatted.tolist()

            else:
                # weird all NA case
                formatted = [pprint_thing(na if isna(x) else x,
                                          escape_chars=('\t', '\r', '\n'))
                             for x in algos.take_1d(lev._values, lab)]
            stringified_levels.append(formatted)

        result_levels = []
        for lev, name in zip(stringified_levels, self.names):
            level = []

            if names:
                level.append(pprint_thing(name,
                                          escape_chars=('\t', '\r', '\n'))
                             if name is not None else '')

            level.extend(np.array(lev, dtype=object))
            result_levels.append(level)

        if sparsify is None:
            sparsify = get_option("display.multi_sparse")

        if sparsify:
            sentinel = ''
            # GH3547
            # use value of sparsify as sentinel,  unless it's an obvious
            # "Truthey" value
            if sparsify not in [True, 1]:
                sentinel = sparsify
            # little bit of a kludge job for #1217
            result_levels = _sparsify(result_levels, start=int(names),
                                      sentinel=sentinel)

        if adjoin:
            from pandas.io.formats.format import _get_adjustment
            adj = _get_adjustment()
            return adj.adjoin(space, *result_levels).split('\n')
        else:
            return result_levels
