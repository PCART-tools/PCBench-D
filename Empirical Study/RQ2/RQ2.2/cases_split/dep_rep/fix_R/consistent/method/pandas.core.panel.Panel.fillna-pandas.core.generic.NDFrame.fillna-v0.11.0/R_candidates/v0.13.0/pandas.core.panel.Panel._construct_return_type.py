    def _construct_return_type(self, result, axes=None, **kwargs):
        """ return the type for the ndim of the result """
        ndim = result.ndim
        if self.ndim == ndim:
            """ return the construction dictionary for these axes """
            if axes is None:
                return self._constructor(result)
            return self._constructor(result, **self._construct_axes_dict())

        elif self.ndim == ndim + 1:
            if axes is None:
                return self._constructor_sliced(result)
            return self._constructor_sliced(
                result, **self._extract_axes_for_slice(self, axes))

        raise PandasError('invalid _construct_return_type [self->%s] '
                          '[result->%s]' % (self.ndim, result.ndim))
