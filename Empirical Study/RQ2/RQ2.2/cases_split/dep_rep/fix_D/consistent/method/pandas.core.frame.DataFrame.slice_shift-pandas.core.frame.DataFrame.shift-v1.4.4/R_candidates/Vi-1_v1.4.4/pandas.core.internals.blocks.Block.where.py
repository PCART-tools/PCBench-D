    def where(self, other, cond) -> list[Block]:
        """
        evaluate the block; return result block(s) from the result

        Parameters
        ----------
        other : a ndarray/object
        cond : np.ndarray[bool], SparseArray[bool], or BooleanArray

        Returns
        -------
        List[Block]
        """
        assert cond.ndim == self.ndim
        assert not isinstance(other, (ABCIndex, ABCSeries, ABCDataFrame))

        transpose = self.ndim == 2

        # EABlocks override where
        values = cast(np.ndarray, self.values)
        orig_other = other
        if transpose:
            values = values.T

        icond, noop = validate_putmask(values, ~cond)
        if noop:
            # GH-39595: Always return a copy; short-circuit up/downcasting
            return self.copy()

        if other is lib.no_default:
            other = self.fill_value

        if is_valid_na_for_dtype(other, self.dtype) and self.dtype != _dtype_obj:
            other = self.fill_value

        if not self._can_hold_element(other):
            # we cannot coerce, return a compat dtype
            block = self.coerce_to_target_dtype(other)
            blocks = block.where(orig_other, cond)
            return self._maybe_downcast(blocks, "infer")

        else:
            alt = setitem_datetimelike_compat(values, icond.sum(), other)
            if alt is not other:
                if is_list_like(other) and len(other) < len(values):
                    # call np.where with other to get the appropriate ValueError
                    np.where(~icond, values, other)
                    raise NotImplementedError(
                        "This should not be reached; call to np.where above is "
                        "expected to raise ValueError. Please report a bug at "
                        "github.com/pandas-dev/pandas"
                    )
                result = values.copy()
                np.putmask(result, icond, alt)
            else:
                # By the time we get here, we should have all Series/Index
                #  args extracted to ndarray
                if (
                    is_list_like(other)
                    and not isinstance(other, np.ndarray)
                    and len(other) == self.shape[-1]
                ):
                    # If we don't do this broadcasting here, then expressions.where
                    #  will broadcast a 1D other to be row-like instead of
                    #  column-like.
                    other = np.array(other).reshape(values.shape)
                    # If lengths don't match (or len(other)==1), we will raise
                    #  inside expressions.where, see test_series_where

                # Note: expressions.where may upcast.
                result = expressions.where(~icond, values, other)

        if self._can_hold_na or self.ndim == 1:

            if transpose:
                result = result.T

            return [self.make_block(result)]

        # might need to separate out blocks
        cond = ~icond
        axis = cond.ndim - 1
        cond = cond.swapaxes(axis, 0)
        mask = cond.all(axis=1)

        result_blocks: list[Block] = []
        for m in [mask, ~mask]:
            if m.any():
                taken = result.take(m.nonzero()[0], axis=axis)
                r = maybe_downcast_numeric(taken, self.dtype)
                if r.dtype != taken.dtype:
                    warnings.warn(
                        "Downcasting integer-dtype results in .where is "
                        "deprecated and will change in a future version. "
                        "To retain the old behavior, explicitly cast the results "
                        "to the desired dtype.",
                        FutureWarning,
                        stacklevel=find_stack_level(),
                    )
                nb = self.make_block(r.T, placement=self._mgr_locs[m])
                result_blocks.append(nb)

        return result_blocks
