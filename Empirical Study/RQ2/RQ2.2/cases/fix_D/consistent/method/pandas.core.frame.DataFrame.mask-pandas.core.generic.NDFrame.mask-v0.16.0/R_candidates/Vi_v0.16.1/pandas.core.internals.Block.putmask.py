    def putmask(self, mask, new, align=True, inplace=False):
        """ putmask the data to the block; it is possible that we may create a
        new dtype of block

        return the resulting block(s)

        Parameters
        ----------
        mask  : the condition to respect
        new : a ndarray/object
        align : boolean, perform alignment on other/cond, default is True
        inplace : perform inplace modification, default is False

        Returns
        -------
        a new block(s), the result of the putmask
        """

        new_values = self.values if inplace else self.values.copy()

        # may need to align the new
        if hasattr(new, 'reindex_axis'):
            new = new.values.T

        # may need to align the mask
        if hasattr(mask, 'reindex_axis'):
            mask = mask.values.T

        # if we are passed a scalar None, convert it here
        if not is_list_like(new) and isnull(new) and not self.is_object:
            new = self.fill_value

        if self._can_hold_element(new):
            new = self._try_cast(new)

            # pseudo-broadcast
            if isinstance(new, np.ndarray) and new.ndim == self.ndim - 1:
                new = np.repeat(new, self.shape[-1]).reshape(self.shape)

            np.putmask(new_values, mask, new)

        # maybe upcast me
        elif mask.any():

            # need to go column by column
            new_blocks = []
            if self.ndim > 1:
                for i, ref_loc in enumerate(self.mgr_locs):
                    m = mask[i]
                    v = new_values[i]

                    # need a new block
                    if m.any():

                        n = new[i] if isinstance(
                            new, np.ndarray) else np.array(new)

                        # type of the new block
                        dtype, _ = com._maybe_promote(n.dtype)

                        # we need to exiplicty astype here to make a copy
                        n = n.astype(dtype)

                        nv = _putmask_smart(v, m, n)
                    else:
                        nv = v if inplace else v.copy()

                    # Put back the dimension that was taken from it and make
                    # a block out of the result.
                    block = make_block(values=nv[np.newaxis],
                                       placement=[ref_loc],
                                       fastpath=True)

                    new_blocks.append(block)

            else:
                nv = _putmask_smart(new_values, mask, new)
                new_blocks.append(make_block(values=nv,
                                             placement=self.mgr_locs,
                                             fastpath=True))

            return new_blocks

        if inplace:
            return [self]

        return [make_block(new_values,
                           placement=self.mgr_locs, fastpath=True)]
