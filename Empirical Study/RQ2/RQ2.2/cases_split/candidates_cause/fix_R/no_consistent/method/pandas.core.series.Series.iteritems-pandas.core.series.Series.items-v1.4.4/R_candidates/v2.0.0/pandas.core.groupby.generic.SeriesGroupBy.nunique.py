    def nunique(self, dropna: bool = True) -> Series | DataFrame:
        """
        Return number of unique elements in the group.

        Returns
        -------
        Series
            Number of unique values within each group.
        """
        ids, _, _ = self.grouper.group_info

        val = self.obj._values

        codes, _ = algorithms.factorize(val, sort=False)
        sorter = np.lexsort((codes, ids))
        codes = codes[sorter]
        ids = ids[sorter]

        # group boundaries are where group ids change
        # unique observations are where sorted values change
        idx = np.r_[0, 1 + np.nonzero(ids[1:] != ids[:-1])[0]]
        inc = np.r_[1, codes[1:] != codes[:-1]]

        # 1st item of each group is a new unique observation
        mask = codes == -1
        if dropna:
            inc[idx] = 1
            inc[mask] = 0
        else:
            inc[mask & np.r_[False, mask[:-1]]] = 0
            inc[idx] = 1

        out = np.add.reduceat(inc, idx).astype("int64", copy=False)
        if len(ids):
            # NaN/NaT group exists if the head of ids is -1,
            # so remove it from res and exclude its index from idx
            if ids[0] == -1:
                res = out[1:]
                idx = idx[np.flatnonzero(idx)]
            else:
                res = out
        else:
            res = out[1:]
        ri = self.grouper.result_index

        # we might have duplications among the bins
        if len(res) != len(ri):
            res, out = np.zeros(len(ri), dtype=out.dtype), res
            if len(ids) > 0:
                # GH#21334s
                res[ids[idx]] = out

        result: Series | DataFrame = self.obj._constructor(
            res, index=ri, name=self.obj.name
        )
        if not self.as_index:
            result = self._insert_inaxis_grouper(result)
            result.index = default_index(len(result))
        return self._reindex_output(result, fill_value=0)
