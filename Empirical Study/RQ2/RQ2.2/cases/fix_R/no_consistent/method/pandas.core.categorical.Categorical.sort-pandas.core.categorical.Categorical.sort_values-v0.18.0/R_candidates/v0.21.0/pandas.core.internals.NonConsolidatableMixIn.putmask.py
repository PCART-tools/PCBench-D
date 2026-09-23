    def putmask(self, mask, new, align=True, inplace=False, axis=0,
                transpose=False, mgr=None):
        """
        putmask the data to the block; we must be a single block and not
        generate other blocks

        return the resulting block

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
        inplace = validate_bool_kwarg(inplace, 'inplace')

        # use block's copy logic.
        # .values may be an Index which does shallow copy by default
        new_values = self.values if inplace else self.copy().values
        new_values, _, new, _ = self._try_coerce_args(new_values, new)

        if isinstance(new, np.ndarray) and len(new) == len(mask):
            new = new[mask]

        mask = _safe_reshape(mask, new_values.shape)

        new_values[mask] = new
        new_values = self._try_coerce_result(new_values)
        return [self.make_block(values=new_values)]
