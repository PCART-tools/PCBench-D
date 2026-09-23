    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        bins=None,
        dropna: bool = True,
    ) -> Series | DataFrame:
        name = "proportion" if normalize else "count"

        if bins is None:
            result = self._value_counts(
                normalize=normalize, sort=sort, ascending=ascending, dropna=dropna
            )
            result.name = name
            return result

        from pandas.core.reshape.merge import get_join_indexers
        from pandas.core.reshape.tile import cut

        ids, _, _ = self.grouper.group_info
        val = self.obj._values

        index_names = self.grouper.names + [self.obj.name]

        if isinstance(val.dtype, CategoricalDtype) or (
            bins is not None and not np.iterable(bins)
        ):
            # scalar bins cannot be done at top level
            # in a backward compatible way
            # GH38672 relates to categorical dtype
            ser = self.apply(
                Series.value_counts,
                normalize=normalize,
                sort=sort,
                ascending=ascending,
                bins=bins,
            )
            ser.name = name
            ser.index.names = index_names
            return ser

        # groupby removes null keys from groupings
        mask = ids != -1
        ids, val = ids[mask], val[mask]

        if bins is None:
            lab, lev = algorithms.factorize(val, sort=True)
            llab = lambda lab, inc: lab[inc]
        else:
            # lab is a Categorical with categories an IntervalIndex
            cat_ser = cut(Series(val, copy=False), bins, include_lowest=True)
            cat_obj = cast("Categorical", cat_ser._values)
            lev = cat_obj.categories
            lab = lev.take(
                cat_obj.codes,
                allow_fill=True,
                fill_value=lev._na_value,
            )
            llab = lambda lab, inc: lab[inc]._multiindex.codes[-1]

        if isinstance(lab.dtype, IntervalDtype):
            # TODO: should we do this inside II?
            lab_interval = cast(Interval, lab)

            sorter = np.lexsort((lab_interval.left, lab_interval.right, ids))
        else:
            sorter = np.lexsort((lab, ids))

        ids, lab = ids[sorter], lab[sorter]

        # group boundaries are where group ids change
        idchanges = 1 + np.nonzero(ids[1:] != ids[:-1])[0]
        idx = np.r_[0, idchanges]
        if not len(ids):
            idx = idchanges

        # new values are where sorted labels change
        lchanges = llab(lab, slice(1, None)) != llab(lab, slice(None, -1))
        inc = np.r_[True, lchanges]
        if not len(val):
            inc = lchanges
        inc[idx] = True  # group boundaries are also new values
        out = np.diff(np.nonzero(np.r_[inc, True])[0])  # value counts

        # num. of times each group should be repeated
        rep = partial(np.repeat, repeats=np.add.reduceat(inc, idx))

        # multi-index components
        codes = self.grouper.reconstructed_codes
        codes = [rep(level_codes) for level_codes in codes] + [llab(lab, inc)]
        levels = [ping.group_index for ping in self.grouper.groupings] + [lev]

        if dropna:
            mask = codes[-1] != -1
            if mask.all():
                dropna = False
            else:
                out, codes = out[mask], [level_codes[mask] for level_codes in codes]

        if normalize:
            out = out.astype("float")
            d = np.diff(np.r_[idx, len(ids)])
            if dropna:
                m = ids[lab == -1]
                np.add.at(d, m, -1)
                acc = rep(d)[mask]
            else:
                acc = rep(d)
            out /= acc

        if sort and bins is None:
            cat = ids[inc][mask] if dropna else ids[inc]
            sorter = np.lexsort((out if ascending else -out, cat))
            out, codes[-1] = out[sorter], codes[-1][sorter]

        if bins is not None:
            # for compat. with libgroupby.value_counts need to ensure every
            # bin is present at every index level, null filled with zeros
            diff = np.zeros(len(out), dtype="bool")
            for level_codes in codes[:-1]:
                diff |= np.r_[True, level_codes[1:] != level_codes[:-1]]

            ncat, nbin = diff.sum(), len(levels[-1])

            left = [np.repeat(np.arange(ncat), nbin), np.tile(np.arange(nbin), ncat)]

            right = [diff.cumsum() - 1, codes[-1]]

            # error: Argument 1 to "get_join_indexers" has incompatible type
            # "List[ndarray[Any, Any]]"; expected "List[Union[Union[ExtensionArray,
            # ndarray[Any, Any]], Index, Series]]
            _, idx = get_join_indexers(
                left, right, sort=False, how="left"  # type: ignore[arg-type]
            )
            out = np.where(idx != -1, out[idx], 0)

            if sort:
                sorter = np.lexsort((out if ascending else -out, left[0]))
                out, left[-1] = out[sorter], left[-1][sorter]

            # build the multi-index w/ full levels
            def build_codes(lev_codes: np.ndarray) -> np.ndarray:
                return np.repeat(lev_codes[diff], nbin)

            codes = [build_codes(lev_codes) for lev_codes in codes[:-1]]
            codes.append(left[-1])

        mi = MultiIndex(
            levels=levels, codes=codes, names=index_names, verify_integrity=False
        )

        if is_integer_dtype(out.dtype):
            out = ensure_int64(out)
        result = self.obj._constructor(out, index=mi, name=name)
        if not self.as_index:
            result = result.reset_index()
        return result
