    @property
    def nbytes(self):
        # TODO: Remove this when we have a DatetimeTZArray
        # Necessary to avoid recursion error since DTI._values is a DTI
        # for TZ-aware
        return self._ndarray_values.nbytes
