    def _str_repeat(self, repeats: int | Sequence[int]):
        if not isinstance(repeats, int):
            raise NotImplementedError(
                f"repeat is not implemented when repeats is {type(repeats).__name__}"
            )
        elif pa_version_under7p0:
            raise NotImplementedError("repeat is not implemented for pyarrow < 7")
        else:
            return type(self)(pc.binary_repeat(self._data, repeats))
