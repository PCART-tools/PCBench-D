    def _validate(self, data):
        if not isinstance(data.dtype, SparseDtype):
            raise AttributeError(self._validation_msg)
