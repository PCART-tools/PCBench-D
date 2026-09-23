    def _cython_agg_blocks(self, how, numeric_only=True):
        data, agg_axis = self._get_data_to_aggregate()

        new_blocks = []

        if numeric_only:
            data = data.get_numeric_data(copy=False)

        for block in data.blocks:
            values = block.values

            is_numeric = is_numeric_dtype(values.dtype)

            if is_numeric:
                values = com.ensure_float(values)

            result, _ = self.grouper.aggregate(values, how, axis=agg_axis)

            # see if we can cast the block back to the original dtype
            result = block._try_cast_result(result)

            newb = make_block(result, placement=block.mgr_locs)
            new_blocks.append(newb)

        if len(new_blocks) == 0:
            raise DataError('No numeric types to aggregate')

        return data.items, new_blocks
