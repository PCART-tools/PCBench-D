    def where(self, other, cond, align=True, errors='raise',
              try_cast=False, axis=0, transpose=False, mgr=None):
        """
        evaluate the block; return result block(s) from the result

        Parameters
        ----------
        other : a ndarray/object
        cond  : the condition to respect
        align : boolean, perform alignment on other/cond
        errors : str, {'raise', 'ignore'}, default 'raise'
            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

        axis : int
        transpose : boolean
            Set to True if self is stored with axes reversed

        Returns
        -------
        a new block(s), the result of the func
        """
        import pandas.core.computation.expressions as expressions
        assert errors in ['raise', 'ignore']

        values = self.values
        orig_other = other
        if transpose:
            values = values.T

        other = getattr(other, 'values', other)
        cond = getattr(cond, 'values', cond)

        # If the default broadcasting would go in the wrong direction, then
        # explicitly reshape other instead
        if getattr(other, 'ndim', 0) >= 1:
            if values.ndim - 1 == other.ndim and axis == 1:
                other = other.reshape(tuple(other.shape + (1, )))

        if not hasattr(cond, 'shape'):
            raise ValueError("where must have a condition that is ndarray "
                             "like")

        # our where function
        def func(cond, values, other):
            if cond.ravel().all():
                return values

            values, values_mask, other, other_mask = self._try_coerce_args(
                values, other)

            try:
                return self._try_coerce_result(expressions.where(
                    cond, values, other))
            except Exception as detail:
                if errors == 'raise':
                    raise TypeError(
                        'Could not operate [{other!r}] with block values '
                        '[{detail!s}]'.format(other=other, detail=detail))
                else:
                    # return the values
                    result = np.empty(values.shape, dtype='float64')
                    result.fill(np.nan)
                    return result

        # see if we can operate on the entire block, or need item-by-item
        # or if we are a single block (ndim == 1)
        try:
            result = func(cond, values, other)
        except TypeError:

            # we cannot coerce, return a compat dtype
            # we are explicitly ignoring errors
            block = self.coerce_to_target_dtype(other)
            blocks = block.where(orig_other, cond, align=align,
                                 errors=errors,
                                 try_cast=try_cast, axis=axis,
                                 transpose=transpose)
            return self._maybe_downcast(blocks, 'infer')

        if self._can_hold_na or self.ndim == 1:

            if transpose:
                result = result.T

            # try to cast if requested
            if try_cast:
                result = self._try_cast_result(result)

            return self.make_block(result)

        # might need to separate out blocks
        axis = cond.ndim - 1
        cond = cond.swapaxes(axis, 0)
        mask = np.array([cond[i].all() for i in range(cond.shape[0])],
                        dtype=bool)

        result_blocks = []
        for m in [mask, ~mask]:
            if m.any():
                r = self._try_cast_result(result.take(m.nonzero()[0],
                                                      axis=axis))
                result_blocks.append(
                    self.make_block(r.T, placement=self.mgr_locs[m]))

        return result_blocks
