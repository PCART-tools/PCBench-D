    def reshape(self: BaseMaskedArrayT, *args, **kwargs) -> BaseMaskedArrayT:
        data = self._data.reshape(*args, **kwargs)
        mask = self._mask.reshape(*args, **kwargs)
        return type(self)(data, mask)
