    def ravel(self: BaseMaskedArrayT, *args, **kwargs) -> BaseMaskedArrayT:
        # TODO: need to make sure we have the same order for data/mask
        data = self._data.ravel(*args, **kwargs)
        mask = self._mask.ravel(*args, **kwargs)
        return type(self)(data, mask)
