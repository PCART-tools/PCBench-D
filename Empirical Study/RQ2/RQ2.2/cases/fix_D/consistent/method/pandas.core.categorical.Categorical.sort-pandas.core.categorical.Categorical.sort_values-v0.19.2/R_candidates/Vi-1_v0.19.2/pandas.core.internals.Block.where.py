    def where(self, other, cond, align=True, raise_on_error=True,
              try_cast=False, axis=0, transpose=False, mgr=None):
        """
        evaluate the block; return result block(s) from the result

        Parameters
        ----------
        other : a ndarray/object
        cond  : the condition to respect
        align : boolean, perform alignment on other/cond
        raise_on_error : if True, raise when I can't perform the function,
            False by default (and just return the data that we had coming in)
        axis : int
        transpose : boolean
            Set to True if self is stored with axes reversed

        Returns
        -------
        a new block(s), the result of the func
        """

        values = self.values
        if transpose:
            values = values.T

        if hasattr(other, 'reindex_axis'):
            other = other.values

        if hasattr(cond, 'reindex_axis'):
            cond = cond.values

        # If the default broadcasting would go in the wrong direction, then
        # explictly reshape other instead
        if getattr(other, 'ndim', 0) >= 1:
            if values.ndim - 1 == other.ndim and axis == 1:
                other = other.reshape(tuple(other.shape + (1, )))

        if not hasattr(cond, 'shape'):
            raise ValueError("where must have a condition that is ndarray "
                             "like")

        other = _maybe_convert_string_to_object(other)
        other = _maybe_convert_scalar(other)

        # our where function
        def func(cond, values, other):
            if cond.ravel().all():
                return values

            values, values_mask, other, other_mask = self._try_coerce_args(
                values, other)
            try:
                return self._try_coerce_result(expressions.where(
                    cond, values, other, raise_on_error=True))
            except Exception as detail:
                if raise_on_error:
                    raise TypeError('Could not operate [%s] with block values '
                                    '[%s]' % (repr(other), str(detail)))
                else:
                    # return the values
                    result = np.empty(values.shape, dtype='float64')
                    result.fill(np.nan)
                    return result

        # see if we can operate on the entire block, or need item-by-item
        # or if we are a single block (ndim == 1)
        result = func(cond, values, other)
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
