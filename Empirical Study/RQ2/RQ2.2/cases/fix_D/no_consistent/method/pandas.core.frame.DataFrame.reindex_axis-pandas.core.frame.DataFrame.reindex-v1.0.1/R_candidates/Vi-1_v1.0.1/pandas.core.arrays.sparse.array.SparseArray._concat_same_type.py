    @classmethod
    def _concat_same_type(cls, to_concat):
        fill_values = [x.fill_value for x in to_concat]

        fill_value = fill_values[0]

        # np.nan isn't a singleton, so we may end up with multiple
        # NaNs here, so we ignore tha all NA case too.
        if not (len(set(fill_values)) == 1 or isna(fill_values).all()):
            warnings.warn(
                "Concatenating sparse arrays with multiple fill "
                f"values: '{fill_values}'. Picking the first and "
                "converting the rest.",
                PerformanceWarning,
                stacklevel=6,
            )
            keep = to_concat[0]
            to_concat2 = [keep]

            for arr in to_concat[1:]:
                to_concat2.append(cls(np.asarray(arr), fill_value=fill_value))

            to_concat = to_concat2

        values = []
        length = 0

        if to_concat:
            sp_kind = to_concat[0].kind
        else:
            sp_kind = "integer"

        if sp_kind == "integer":
            indices = []

            for arr in to_concat:
                idx = arr.sp_index.to_int_index().indices.copy()
                idx += length  # TODO: wraparound
                length += arr.sp_index.length

                values.append(arr.sp_values)
                indices.append(idx)

            data = np.concatenate(values)
            indices = np.concatenate(indices)
            sp_index = IntIndex(length, indices)

        else:
            # when concatenating block indices, we don't claim that you'll
            # get an identical index as concating the values and then
            # creating a new index. We don't want to spend the time trying
            # to merge blocks across arrays in `to_concat`, so the resulting
            # BlockIndex may have more blocs.
            blengths = []
            blocs = []

            for arr in to_concat:
                idx = arr.sp_index.to_block_index()

                values.append(arr.sp_values)
                blocs.append(idx.blocs.copy() + length)
                blengths.append(idx.blengths)
                length += arr.sp_index.length

            data = np.concatenate(values)
            blocs = np.concatenate(blocs)
            blengths = np.concatenate(blengths)

            sp_index = BlockIndex(length, blocs, blengths)

        return cls(data, sparse_index=sp_index, fill_value=fill_value)
