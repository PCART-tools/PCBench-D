    def __array__(self, dtype=None, copy=None):
        if dtype is not None and dtype != self._array.dtype:
            if copy is not None and not copy:
                raise ValueError(
                    f"Converting array from {self._array.dtype} to "
                    f"{dtype} requires a copy"
                )

        arr = np.asarray(self._array, dtype=dtype)
        return (arr if not copy else np.copy(arr))
