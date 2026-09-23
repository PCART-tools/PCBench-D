    def where(self, other, cond, align=True, raise_on_error=True,
              try_cast=False):
        """
        evaluate the block; return result block(s) from the result

        Parameters
        ----------
        other : a ndarray/object
        cond  : the condition to respect
        align : boolean, perform alignment on other/cond
        raise_on_error : if True, raise when I can't perform the function,
            False by default (and just return the data that we had coming in)

        Returns
        -------
        a new block(s), the result of the func
        """

        values = self.values

        # see if we can align other
        if hasattr(other, 'reindex_axis'):
            other = other.values

        # make sure that we can broadcast
        is_transposed = False
        if hasattr(other, 'ndim') and hasattr(values, 'ndim'):
            if values.ndim != other.ndim or values.shape == other.shape[::-1]:

                # pseodo broadcast (its a 2d vs 1d say and where needs it in a
                # specific direction)
                if (other.ndim >= 1 and values.ndim - 1 == other.ndim and
                        values.shape[0] != other.shape[0]):
                    other = _block_shape(other).T
                else:
                    values = values.T
                    is_transposed = True

        # see if we can align cond
        if not hasattr(cond, 'shape'):
            raise ValueError(
                "where must have a condition that is ndarray like")

        if hasattr(cond, 'reindex_axis'):
            cond = cond.values

        # may need to undo transpose of values
        if hasattr(values, 'ndim'):
            if values.ndim != cond.ndim or values.shape == cond.shape[::-1]:
                values = values.T
                is_transposed = not is_transposed

        # our where function
        def func(c, v, o):
            if c.ravel().all():
                return v

            v, o = self._try_coerce_args(v, o)
            try:
                return self._try_coerce_result(
                    expressions.where(c, v, o, raise_on_error=True)
                )
            except Exception as detail:
                if raise_on_error:
                    raise TypeError('Could not operate [%s] with block values '
                                    '[%s]' % (repr(o), str(detail)))
                else:
                    # return the values
                    result = np.empty(v.shape, dtype='float64')
                    result.fill(np.nan)
                    return result

        # see if we can operate on the entire block, or need item-by-item
        # or if we are a single block (ndim == 1)
        result = func(cond, values, other)
        if self._can_hold_na or self.ndim == 1:

            if not isinstance(result, np.ndarray):
                raise TypeError('Could not compare [%s] with block values'
                                % repr(other))

            if is_transposed:
                result = result.T

            # try to cast if requested
            if try_cast:
                result = self._try_cast_result(result)

            return make_block(result,
                              ndim=self.ndim, placement=self.mgr_locs)

        # might need to separate out blocks
        axis = cond.ndim - 1
        cond = cond.swapaxes(axis, 0)
        mask = np.array([cond[i].all() for i in range(cond.shape[0])],
                        dtype=bool)

        result_blocks = []
        for m in [mask, ~mask]:
            if m.any():
                r = self._try_cast_result(
                    result.take(m.nonzero()[0], axis=axis))
                result_blocks.append(make_block(r.T,
                                                placement=self.mgr_locs[m]))

        return result_blocks
