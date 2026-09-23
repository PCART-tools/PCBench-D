    def format(
        self,
        name: Optional[bool] = None,
        formatter: Optional[Callable] = None,
        na_rep: Optional[str] = None,
        names: bool = False,
        space: int = 2,
        sparsify=None,
        adjoin: bool = True,
    ) -> List:
        if name is not None:
            names = name

        if len(self) == 0:
            return []

        stringified_levels = []
        for lev, level_codes in zip(self.levels, self.codes):
            na = na_rep if na_rep is not None else _get_na_rep(lev.dtype.type)

            if len(lev) > 0:

                formatted = lev.take(level_codes).format(formatter=formatter)

                # we have some NA
                mask = level_codes == -1
                if mask.any():
                    formatted = np.array(formatted, dtype=object)
                    formatted[mask] = na
                    formatted = formatted.tolist()

            else:
                # weird all NA case
                formatted = [
                    pprint_thing(na if isna(x) else x, escape_chars=("\t", "\r", "\n"))
                    for x in algos.take_1d(lev._values, level_codes)
                ]
            stringified_levels.append(formatted)

        result_levels = []
        for lev, lev_name in zip(stringified_levels, self.names):
            level = []

            if names:
                level.append(
                    pprint_thing(lev_name, escape_chars=("\t", "\r", "\n"))
                    if lev_name is not None
                    else ""
                )

            level.extend(np.array(lev, dtype=object))
            result_levels.append(level)

        if sparsify is None:
            sparsify = get_option("display.multi_sparse")

        if sparsify:
            sentinel = ""
            # GH3547 use value of sparsify as sentinel if it's "Falsey"
            assert isinstance(sparsify, bool) or sparsify is lib.no_default
            if sparsify in [False, lib.no_default]:
                sentinel = sparsify
            # little bit of a kludge job for #1217
            result_levels = sparsify_labels(
                result_levels, start=int(names), sentinel=sentinel
            )

        if adjoin:
            from pandas.io.formats.format import get_adjustment

            adj = get_adjustment()
            return adj.adjoin(space, *result_levels).split("\n")
        else:
            return result_levels
