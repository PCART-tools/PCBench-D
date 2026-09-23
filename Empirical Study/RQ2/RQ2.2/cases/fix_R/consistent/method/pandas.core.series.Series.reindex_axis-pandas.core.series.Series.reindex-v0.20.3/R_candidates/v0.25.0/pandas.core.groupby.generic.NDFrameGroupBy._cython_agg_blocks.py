    def _cython_agg_blocks(self, how, alt=None, numeric_only=True, min_count=-1):
        # TODO: the actual managing of mgr_locs is a PITA
        # here, it should happen via BlockManager.combine

        data, agg_axis = self._get_data_to_aggregate()

        if numeric_only:
            data = data.get_numeric_data(copy=False)

        new_blocks = []
        new_items = []
        deleted_items = []
        for block in data.blocks:

            locs = block.mgr_locs.as_array
            try:
                result, _ = self.grouper.aggregate(
                    block.values, how, axis=agg_axis, min_count=min_count
                )
            except NotImplementedError:
                # generally if we have numeric_only=False
                # and non-applicable functions
                # try to python agg

                if alt is None:
                    # we cannot perform the operation
                    # in an alternate way, exclude the block
                    deleted_items.append(locs)
                    continue

                # call our grouper again with only this block
                from pandas.core.groupby.groupby import groupby

                obj = self.obj[data.items[locs]]
                s = groupby(obj, self.grouper)
                try:
                    result = s.aggregate(lambda x: alt(x, axis=self.axis))
                except TypeError:
                    # we may have an exception in trying to aggregate
                    # continue and exclude the block
                    pass

            finally:

                dtype = block.values.dtype

                # see if we can cast the block back to the original dtype
                result = block._try_coerce_and_cast_result(result, dtype=dtype)
                newb = block.make_block(result)

            new_items.append(locs)
            new_blocks.append(newb)

        if len(new_blocks) == 0:
            raise DataError("No numeric types to aggregate")

        # reset the locs in the blocks to correspond to our
        # current ordering
        indexer = np.concatenate(new_items)
        new_items = data.items.take(np.sort(indexer))

        if len(deleted_items):

            # we need to adjust the indexer to account for the
            # items we have removed
            # really should be done in internals :<

            deleted = np.concatenate(deleted_items)
            ai = np.arange(len(data))
            mask = np.zeros(len(data))
            mask[deleted] = 1
            indexer = (ai - mask.cumsum())[indexer]

        offset = 0
        for b in new_blocks:
            loc = len(b.mgr_locs)
            b.mgr_locs = indexer[offset : (offset + loc)]
            offset += loc

        return new_items, new_blocks
