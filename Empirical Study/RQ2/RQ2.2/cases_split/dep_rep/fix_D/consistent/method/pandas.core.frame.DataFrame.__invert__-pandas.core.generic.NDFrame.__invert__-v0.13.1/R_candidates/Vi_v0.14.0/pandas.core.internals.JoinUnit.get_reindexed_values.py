    def get_reindexed_values(self, empty_dtype, upcasted_na):
        if upcasted_na is None:
            # No upcasting is necessary
            fill_value = self.block.fill_value
            values = self.block.get_values()
        else:
            fill_value = upcasted_na

            if self.is_null:
                missing_arr = np.empty(self.shape, dtype=empty_dtype)
                if np.prod(self.shape):
                    # NumPy 1.6 workaround: this statement gets strange if all
                    # blocks are of same dtype and some of them are empty:
                    # empty one are considered "null" so they must be filled,
                    # but no dtype upcasting happens and the dtype may not
                    # allow NaNs.
                    #
                    # In general, no one should get hurt when one tries to put
                    # incorrect values into empty array, but numpy 1.6 is
                    # strict about that.
                    missing_arr.fill(fill_value)
                return missing_arr

            if self.block.is_bool:
                # External code requested filling/upcasting, bool values must
                # be upcasted to object to avoid being upcasted to numeric.
                values = self.block.astype(np.object_).values
            else:
                # No dtype upcasting is done here, it will be performed during
                # concatenation itself.
                values = self.block.get_values()

        if not self.indexers:
            # If there's no indexing to be done, we want to signal outside
            # code that this array must be copied explicitly.  This is done
            # by returning a view and checking `retval.base`.
            return values.view()
        else:
            for ax, indexer in self.indexers.items():
                values = com.take_nd(values, indexer, axis=ax,
                                     fill_value=fill_value)

            return values
