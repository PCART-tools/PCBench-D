    def _delegate_method(self, name: str, *args, **kwargs):
        if not hasattr(self._parent.array, f"_dt_{name}"):
            raise NotImplementedError(
                f"dt.{name} is not supported for {self._parent.dtype}"
            )

        result = getattr(self._parent.array, f"_dt_{name}")(*args, **kwargs)

        if self._orig is not None:
            index = self._orig.index
        else:
            index = self._parent.index
        # return the result as a Series, which is by definition a copy
        result = type(self._parent)(
            result, index=index, name=self._parent.name
        ).__finalize__(self._parent)

        return result
