    def eval(self, func, other, errors='raise', try_cast=False, mgr=None):
        """
        evaluate the block; return result block from the result

        Parameters
        ----------
        func  : how to combine self, other
        other : a ndarray/object
        errors : str, {'raise', 'ignore'}, default 'raise'
            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

        try_cast : try casting the results to the input type

        Returns
        -------
        a new block, the result of the func
        """
        orig_other = other
        values = self.values

        other = getattr(other, 'values', other)

        # make sure that we can broadcast
        is_transposed = False
        if hasattr(other, 'ndim') and hasattr(values, 'ndim'):
            if values.ndim != other.ndim:
                is_transposed = True
            else:
                if values.shape == other.shape[::-1]:
                    is_transposed = True
                elif values.shape[0] == other.shape[-1]:
                    is_transposed = True
                else:
                    # this is a broadcast error heree
                    raise ValueError(
                        "cannot broadcast shape [{t_shape}] with "
                        "block values [{oth_shape}]".format(
                            t_shape=values.T.shape, oth_shape=other.shape))

        transf = (lambda x: x.T) if is_transposed else (lambda x: x)

        # coerce/transpose the args if needed
        try:
            values, values_mask, other, other_mask = self._try_coerce_args(
                transf(values), other)
        except TypeError:
            block = self.coerce_to_target_dtype(orig_other)
            return block.eval(func, orig_other,
                              errors=errors,
                              try_cast=try_cast, mgr=mgr)

        # get the result, may need to transpose the other
        def get_result(other):

            # avoid numpy warning of comparisons again None
            if other is None:
                result = not func.__name__ == 'eq'

            # avoid numpy warning of elementwise comparisons to object
            elif is_numeric_v_string_like(values, other):
                result = False

            # avoid numpy warning of elementwise comparisons
            elif func.__name__ == 'eq':
                if is_list_like(other) and not isinstance(other, np.ndarray):
                    other = np.asarray(other)

                    # if we can broadcast, then ok
                    if values.shape[-1] != other.shape[-1]:
                        return False
                result = func(values, other)
            else:
                result = func(values, other)

            # mask if needed
            if isinstance(values_mask, np.ndarray) and values_mask.any():
                result = result.astype('float64', copy=False)
                result[values_mask] = np.nan
            if other_mask is True:
                result = result.astype('float64', copy=False)
                result[:] = np.nan
            elif isinstance(other_mask, np.ndarray) and other_mask.any():
                result = result.astype('float64', copy=False)
                result[other_mask.ravel()] = np.nan

            return result

        # error handler if we have an issue operating with the function
        def handle_error():

            if errors == 'raise':
                # The 'detail' variable is defined in outer scope.
                raise TypeError(
                    'Could not operate {other!r} with block values '
                    '{detail!s}'.format(other=other, detail=detail))  # noqa
            else:
                # return the values
                result = np.empty(values.shape, dtype='O')
                result.fill(np.nan)
                return result

        # get the result
        try:
            with np.errstate(all='ignore'):
                result = get_result(other)

        # if we have an invalid shape/broadcast error
        # GH4576, so raise instead of allowing to pass through
        except ValueError as detail:
            raise
        except Exception as detail:
            result = handle_error()

        # technically a broadcast error in numpy can 'work' by returning a
        # boolean False
        if not isinstance(result, np.ndarray):
            if not isinstance(result, np.ndarray):

                # differentiate between an invalid ndarray-ndarray comparison
                # and an invalid type comparison
                if isinstance(values, np.ndarray) and is_list_like(other):
                    raise ValueError(
                        'Invalid broadcasting comparison [{other!r}] with '
                        'block values'.format(other=other))

                raise TypeError('Could not compare [{other!r}] '
                                'with block values'.format(other=other))

        # transpose if needed
        result = transf(result)

        # try to cast if requested
        if try_cast:
            result = self._try_cast_result(result)

        result = _block_shape(result, ndim=self.ndim)
        return [self.make_block(result)]
