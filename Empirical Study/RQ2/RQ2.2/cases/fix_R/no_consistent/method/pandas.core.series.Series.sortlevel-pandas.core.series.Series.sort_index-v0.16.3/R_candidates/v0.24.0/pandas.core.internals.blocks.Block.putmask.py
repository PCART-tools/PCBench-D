    def putmask(self, mask, new, align=True, inplace=False, axis=0,
                transpose=False):
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

        new = getattr(new, 'values', new)
        mask = getattr(mask, 'values', mask)

        # if we are passed a scalar None, convert it here
        if not is_list_like(new) and isna(new) and not self.is_object:
            new = self.fill_value

        if self._can_hold_element(new):
            _, new = self._try_coerce_args(new_values, new)

            if transpose:
                new_values = new_values.T

            # If the default repeat behavior in np.putmask would go in the
            # wrong direction, then explicitly repeat and reshape new instead
            if getattr(new, 'ndim', 0) >= 1:
                if self.ndim - 1 == new.ndim and axis == 1:
                    new = np.repeat(
                        new, new_values.shape[-1]).reshape(self.shape)
                new = new.astype(new_values.dtype)

            # we require exact matches between the len of the
            # values we are setting (or is compat). np.putmask
            # doesn't check this and will simply truncate / pad
            # the output, but we want sane error messages
            #
            # TODO: this prob needs some better checking
            # for 2D cases
            if ((is_list_like(new) and
                 np.any(mask[mask]) and
                 getattr(new, 'ndim', 1) == 1)):

                if not (mask.shape[-1] == len(new) or
                        mask[mask].shape[-1] == len(new) or
                        len(new) == 1):
                    raise ValueError("cannot assign mismatch "
                                     "length to masked array")

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

            # operate column-by-column
            def f(m, v, i):

                if i is None:
                    # ndim==1 case.
                    n = new
                else:

                    if isinstance(new, np.ndarray):
                        n = np.squeeze(new[i % new.shape[0]])
                    else:
                        n = np.array(new)

                    # type of the new block
                    dtype, _ = maybe_promote(n.dtype)

                    # we need to explicitly astype here to make a copy
                    n = n.astype(dtype)

                nv = _putmask_smart(v, m, n)
                return nv

            new_blocks = self.split_and_operate(mask, f, inplace)
            return new_blocks

        if inplace:
            return [self]

        if transpose:
            new_values = new_values.T

        return [self.make_block(new_values)]
