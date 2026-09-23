    def putmask(self, mask, new) -> list[Block]:
        """
        putmask the data to the block; it is possible that we may create a
        new dtype of block

        Return the resulting block(s).

        Parameters
        ----------
        mask : np.ndarray[bool], SparseArray[bool], or BooleanArray
        new : a ndarray/object

        Returns
        -------
        List[Block]
        """
        orig_mask = mask
        values = cast(np.ndarray, self.values)
        mask, noop = validate_putmask(values.T, mask)
        assert not isinstance(new, (ABCIndex, ABCSeries, ABCDataFrame))

        if new is lib.no_default:
            new = self.fill_value

        # if we are passed a scalar None, convert it here
        if not self.is_object and is_valid_na_for_dtype(new, self.dtype):
            new = self.fill_value

        if self._can_hold_element(new):
            putmask_without_repeat(values.T, mask, new)
            return [self]

        elif np_version_under1p20 and infer_dtype_from(new)[0].kind in ["m", "M"]:
            # using putmask with object dtype will incorrectly cast to object
            # Having excluded self._can_hold_element, we know we cannot operate
            #  in-place, so we are safe using `where`
            return self.where(new, ~mask)

        elif noop:
            return [self]

        elif self.ndim == 1 or self.shape[0] == 1:
            # no need to split columns

            if not is_list_like(new):
                # putmask_smart can't save us the need to cast
                return self.coerce_to_target_dtype(new).putmask(mask, new)

            # This differs from
            #  `self.coerce_to_target_dtype(new).putmask(mask, new)`
            # because putmask_smart will check if new[mask] may be held
            # by our dtype.
            nv = putmask_smart(values.T, mask, new).T
            return [self.make_block(nv)]

        else:
            is_array = isinstance(new, np.ndarray)

            res_blocks = []
            nbs = self._split()
            for i, nb in enumerate(nbs):
                n = new
                if is_array:
                    # we have a different value per-column
                    n = new[:, i : i + 1]

                submask = orig_mask[:, i : i + 1]
                rbs = nb.putmask(submask, n)
                res_blocks.extend(rbs)
            return res_blocks
