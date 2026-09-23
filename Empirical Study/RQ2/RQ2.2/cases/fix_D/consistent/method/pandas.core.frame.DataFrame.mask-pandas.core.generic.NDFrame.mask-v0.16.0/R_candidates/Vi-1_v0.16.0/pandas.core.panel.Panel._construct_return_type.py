    def _construct_return_type(self, result, axes=None):
        """ return the type for the ndim of the result """
        ndim = getattr(result,'ndim',None)

        # need to assume they are the same
        if ndim is None:
            if isinstance(result,dict):
                ndim = getattr(list(compat.itervalues(result))[0],'ndim',None)

                # a saclar result
                if ndim is None:
                    ndim = 0

                # have a dict, so top-level is +1 dim
                else:
                    ndim += 1

        # scalar
        if ndim == 0:
            return Series(result)

        # same as self
        elif self.ndim == ndim:
            """ return the construction dictionary for these axes """
            if axes is None:
                return self._constructor(result)
            return self._constructor(result, **self._construct_axes_dict())

        # sliced
        elif self.ndim == ndim + 1:
            if axes is None:
                return self._constructor_sliced(result)
            return self._constructor_sliced(
                result, **self._extract_axes_for_slice(self, axes))

        raise PandasError('invalid _construct_return_type [self->%s] '
                          '[result->%s]' % (self, result))
