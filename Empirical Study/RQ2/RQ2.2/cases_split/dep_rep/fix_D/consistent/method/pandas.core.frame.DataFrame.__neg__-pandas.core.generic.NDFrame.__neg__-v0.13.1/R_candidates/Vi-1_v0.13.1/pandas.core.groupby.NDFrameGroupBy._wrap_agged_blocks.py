    def _wrap_agged_blocks(self, blocks):
        obj = self._obj_with_exclusions

        new_axes = list(obj._data.axes)

        # more kludge
        if self.axis == 0:
            new_axes[0], new_axes[1] = new_axes[1], self.grouper.result_index
        else:
            new_axes[self.axis] = self.grouper.result_index

        mgr = BlockManager(blocks, new_axes)

        new_obj = type(obj)(mgr)

        return self._post_process_cython_aggregate(new_obj)
