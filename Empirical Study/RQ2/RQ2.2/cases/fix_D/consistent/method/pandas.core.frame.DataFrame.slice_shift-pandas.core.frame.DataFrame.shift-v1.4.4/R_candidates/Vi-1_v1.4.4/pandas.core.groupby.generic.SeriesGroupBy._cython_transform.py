    def _cython_transform(
        self, how: str, numeric_only: bool = True, axis: int = 0, **kwargs
    ):
        assert axis == 0  # handled by caller

        obj = self._selected_obj

        try:
            result = self.grouper._cython_operation(
                "transform", obj._values, how, axis, **kwargs
            )
        except NotImplementedError as err:
            raise TypeError(f"{how} is not supported for {obj.dtype} dtype") from err

        return obj._constructor(result, index=self.obj.index, name=obj.name)
