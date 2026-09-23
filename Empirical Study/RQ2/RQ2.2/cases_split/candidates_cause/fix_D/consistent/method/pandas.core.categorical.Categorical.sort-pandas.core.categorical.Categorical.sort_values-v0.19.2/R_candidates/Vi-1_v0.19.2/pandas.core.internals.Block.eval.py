    def eval(self, func, other, raise_on_error=True, try_cast=False, mgr=None):
        """
        evaluate the block; return result block from the result

        Parameters
        ----------
        func  : how to combine self, other
        other : a ndarray/object
        raise_on_error : if True, raise when I can't perform the function,
            False by default (and just return the data that we had coming in)
        try_cast : try casting the results to the input type

        Returns
        -------
        a new block, the result of the func
        """
        values = self.values

        if hasattr(other, 'reindex_axis'):
            other = other.values

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
                    raise ValueError("cannot broadcast shape [%s] with block "
                                     "values [%s]" % (values.T.shape,
                                                      other.shape))

        transf = (lambda x: x.T) if is_transposed else (lambda x: x)

        # coerce/transpose the args if needed
        values, values_mask, other, other_mask = self._try_coerce_args(
            transf(values), other)

        # get the result, may need to transpose the other
        def get_result(other):

            # avoid numpy warning of comparisons again None
            if other is None:
                result = not func.__name__ == 'eq'

            # avoid numpy warning of elementwise comparisons to object
            elif is_numeric_v_string_like(values, other):
                result = False

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

            return self._try_coerce_result(result)

        # error handler if we have an issue operating with the function
        def handle_error():

            if raise_on_error:
                raise TypeError('Could not operate %s with block values %s' %
                                (repr(other), str(detail)))
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
                    raise ValueError('Invalid broadcasting comparison [%s] '
                                     'with block values' % repr(other))

                raise TypeError('Could not compare [%s] with block values' %
                                repr(other))

        # transpose if needed
        result = transf(result)

        # try to cast if requested
        if try_cast:
            result = self._try_cast_result(result)

        return [self.make_block(result, fastpath=True, )]
