    def _nth(
        self,
        n: PositionalIndexer | tuple,
        dropna: Literal["any", "all", None] = None,
    ) -> NDFrameT:
        if not dropna:
            mask = self._make_mask_from_positional_indexer(n)

            ids, _, _ = self.grouper.group_info

            # Drop NA values in grouping
            mask = mask & (ids != -1)

            out = self._mask_selected_obj(mask)
            return out

        # dropna is truthy
        if not is_integer(n):
            raise ValueError("dropna option only supported for an integer argument")

        if dropna not in ["any", "all"]:
            # Note: when agg-ing picker doesn't raise this, just returns NaN
            raise ValueError(
                "For a DataFrame or Series groupby.nth, dropna must be "
                "either None, 'any' or 'all', "
                f"(was passed {dropna})."
            )

        # old behaviour, but with all and any support for DataFrames.
        # modified in GH 7559 to have better perf
        n = cast(int, n)
        dropped = self.obj.dropna(how=dropna, axis=self.axis)

        # get a new grouper for our dropped obj
        if self.keys is None and self.level is None:
            # we don't have the grouper info available
            # (e.g. we have selected out
            # a column that is not in the current object)
            axis = self.grouper.axis
            grouper = self.grouper.codes_info[axis.isin(dropped.index)]
            if self.grouper.has_dropped_na:
                # Null groups need to still be encoded as -1 when passed to groupby
                nulls = grouper == -1
                # error: No overload variant of "where" matches argument types
                #        "Any", "NAType", "Any"
                values = np.where(nulls, NA, grouper)  # type: ignore[call-overload]
                grouper = Index(values, dtype="Int64")

        else:
            # create a grouper with the original parameters, but on dropped
            # object
            grouper, _, _ = get_grouper(
                dropped,
                key=self.keys,
                axis=self.axis,
                level=self.level,
                sort=self.sort,
            )

        grb = dropped.groupby(
            grouper, as_index=self.as_index, sort=self.sort, axis=self.axis
        )
        return grb.nth(n)
