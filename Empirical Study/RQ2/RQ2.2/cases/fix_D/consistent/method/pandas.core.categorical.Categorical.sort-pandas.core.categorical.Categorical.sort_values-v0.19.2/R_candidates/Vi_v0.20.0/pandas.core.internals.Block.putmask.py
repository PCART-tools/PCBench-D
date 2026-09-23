    def putmask(self, mask, new, align=True, inplace=False, axis=0,
                transpose=False, mgr=None):
        """ putmask the data to the block; it is possible that we may create a
        new dtype of block

        return the resulting block(s)

        Parameters
        ----------
        mask  : the condition to respect
        new : a ndarray/object
        align : boolean, perform alignment on other/cond, default is True
        inplace : perform inplace modification, default is False
        axis : int
        transpose : boolean
            Set to True if self is stored with axes reversed

        Returns
        -------
        a list of new blocks, the result of the putmask
        """

        new_values = self.values if inplace else self.values.copy()

        if hasattr(new, 'reindex_axis'):
            new = new.values

        if hasattr(mask, 'reindex_axis'):
            mask = mask.values

        # if we are passed a scalar None, convert it here
        if not is_list_like(new) and isnull(new) and not self.is_object:
            new = self.fill_value

        if self._can_hold_element(new):
            if transpose:
                new_values = new_values.T

            new = self._try_cast(new)

            # If the default repeat behavior in np.putmask would go in the
            # wrong direction, then explictly repeat and reshape new instead
            if getattr(new, 'ndim', 0) >= 1:
                if self.ndim - 1 == new.ndim and axis == 1:
                    new = np.repeat(
                        new, new_values.shape[-1]).reshape(self.shape)
                new = new.astype(new_values.dtype)

            np.putmask(new_values, mask, new)

        # maybe upcast me
        elif mask.any():
            if transpose:
                mask = mask.T
                if isinstance(new, np.ndarray):
                    new = new.T
                axis = new_values.ndim - axis - 1

            # Pseudo-broadcast
            if getattr(new, 'ndim', 0) >= 1:
                if self.ndim - 1 == new.ndim:
                    new_shape = list(new.shape)
                    new_shape.insert(axis, 1)
                    new = new.reshape(tuple(new_shape))

            # need to go column by column
            new_blocks = []
            if self.ndim > 1:
                for i, ref_loc in enumerate(self.mgr_locs):
                    m = mask[i]
                    v = new_values[i]

                    # need a new block
                    if m.any():
                        if isinstance(new, np.ndarray):
                            n = np.squeeze(new[i % new.shape[0]])
                        else:
                            n = np.array(new)

                        # type of the new block
                        dtype, _ = maybe_promote(n.dtype)

                        # we need to explicitly astype here to make a copy
                        n = n.astype(dtype)

                        nv = _putmask_smart(v, m, n)
                    else:
                        nv = v if inplace else v.copy()

                    # Put back the dimension that was taken from it and make
                    # a block out of the result.
                    block = self.make_block(values=nv[np.newaxis],
                                            placement=[ref_loc], fastpath=True)

                    new_blocks.append(block)

            else:
                nv = _putmask_smart(new_values, mask, new)
                new_blocks.append(self.make_block(values=nv, fastpath=True))

            return new_blocks

        if inplace:
            return [self]

        if transpose:
            new_values = new_values.T

        return [self.make_block(new_values, fastpath=True)]
