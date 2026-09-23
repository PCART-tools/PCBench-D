    def astype(self, dtype, copy=False, raise_on_error=True):
        """
        handle convert to object as a special case
        """
        klass = None
        if np.dtype(dtype).type == np.object_:
            klass = ObjectBlock
        return self._astype(dtype, copy=copy, raise_on_error=raise_on_error,
                            klass=klass)
