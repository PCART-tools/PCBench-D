    def _delegate_property_get(self, name: str):  # type: ignore[override]
        if not hasattr(self._parent.array, f"_dt_{name}"):
            raise NotImplementedError(
                f"dt.{name} is not supported for {self._parent.dtype}"
            )
        result = getattr(self._parent.array, f"_dt_{name}")

        if not is_list_like(result):
            return result

        if self._orig is not None:
            index = self._orig.index
        else:
            index = self._parent.index
        # return the result as a Series, which is by definition a copy
        result = type(self._parent)(
            result, index=index, name=self._parent.name
        ).__finalize__(self._parent)

        return result
