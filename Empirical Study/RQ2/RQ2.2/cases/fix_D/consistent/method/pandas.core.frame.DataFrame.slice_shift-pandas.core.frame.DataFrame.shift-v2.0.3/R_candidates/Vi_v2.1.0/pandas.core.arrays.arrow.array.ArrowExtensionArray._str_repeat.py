    def _str_repeat(self, repeats: int | Sequence[int]):
        if not isinstance(repeats, int):
            raise NotImplementedError(
                f"repeat is not implemented when repeats is {type(repeats).__name__}"
            )
        else:
            return type(self)(pc.binary_repeat(self._pa_array, repeats))
