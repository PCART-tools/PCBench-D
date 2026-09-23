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
            if align:
                axis = getattr(new, '_info_axis_number', 0)
                new = new.reindex_axis(self.items, axis=axis,
                                       copy=False).values.T
            else:
                new = new.values.T

        # may need to align the mask
        if hasattr(mask, 'reindex_axis'):
            if align:
                axis = getattr(mask, '_info_axis_number', 0)
                mask = mask.reindex_axis(
                    self.items, axis=axis, copy=False).values.T
            else:
                mask = mask.values.T

        # if we are passed a scalar None, convert it here
        if not is_list_like(new) and isnull(new):
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

            def create_block(v, m, n, item, reshape=True):
                """ return a new block, try to preserve dtype if possible """

                # n should the length of the mask or a scalar here
                if not is_list_like(n):
                    n = np.array([n] * len(m))

                # see if we are only masking values that if putted
                # will work in the current dtype
                nv = None
                try:
                    nn = n[m]
                    nn_at = nn.astype(self.dtype)
                    if (nn == nn_at).all():
                        nv = v.copy()
                        nv[mask] = nn_at
                except:
                    pass

                # change the dtype
                if nv is None:
                    dtype, _ = com._maybe_promote(n.dtype)
                    nv = v.astype(dtype)
                    try:
                        nv[m] = n
                    except:
                        np.putmask(nv, m, n)

                if reshape:
                    nv = _block_shape(nv)
                    return make_block(nv, [item], self.ref_items)
                else:
                    return make_block(nv, item, self.ref_items)

            if self.ndim > 1:
                for i, item in enumerate(self.items):
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

                        block = create_block(v, m, n, item)

                    else:
                        nv = v if inplace else v.copy()
                        nv = _block_shape(nv)
                        block = make_block(
                            nv, Index([item]), self.ref_items, fastpath=True)

                    new_blocks.append(block)

            else:
                new_blocks.append(create_block(new_values, mask, new,
                                               self.items, reshape=False))

            return new_blocks

        if inplace:
            return [self]

        return [make_block(new_values, self.items, self.ref_items,
                           placement=self._ref_locs, fastpath=True)]
