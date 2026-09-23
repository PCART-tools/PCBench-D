    def shift(self: T, periods: int, axis: int, fill_value) -> T:
        axis = self._normalize_axis(axis)
        if fill_value is lib.no_default:
            fill_value = None

        if (
            axis == 0
            and self.ndim == 2
            and (
                self.nblocks > 1
                or (
                    # If we only have one block and we know that we can't
                    #  keep the same dtype (i.e. the _can_hold_element check)
                    #  then we can go through the reindex_indexer path
                    #  (and avoid casting logic in the Block method).
                    #  The exception to this (until 2.0) is datetimelike
                    #  dtypes with integers, which cast.
                    not self.blocks[0]._can_hold_element(fill_value)
                    # TODO(2.0): remove special case for integer-with-datetimelike
                    #  once deprecation is enforced
                    and not (
                        lib.is_integer(fill_value)
                        and needs_i8_conversion(self.blocks[0].dtype)
                    )
                )
            )
        ):
            # GH#35488 we need to watch out for multi-block cases
            # We only get here with fill_value not-lib.no_default
            ncols = self.shape[0]
            nper = abs(periods)
            nper = min(nper, ncols)
            if periods > 0:
                indexer = np.array(
                    [-1] * nper + list(range(ncols - periods)), dtype=np.intp
                )
            else:
                indexer = np.array(
                    list(range(nper, ncols)) + [-1] * nper, dtype=np.intp
                )
            result = self.reindex_indexer(
                self.items,
                indexer,
                axis=0,
                fill_value=fill_value,
                allow_dups=True,
                consolidate=False,
            )
            return result

        return self.apply("shift", periods=periods, axis=axis, fill_value=fill_value)
