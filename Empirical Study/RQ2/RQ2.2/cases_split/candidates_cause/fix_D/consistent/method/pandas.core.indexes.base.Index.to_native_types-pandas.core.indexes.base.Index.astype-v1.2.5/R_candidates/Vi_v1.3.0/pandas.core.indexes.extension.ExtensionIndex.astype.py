    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True) -> Index:
        dtype = pandas_dtype(dtype)
        if is_dtype_equal(self.dtype, dtype):
            if not copy:
                # Ensure that self.astype(self.dtype) is self
                return self
            return self.copy()

        # error: Non-overlapping equality check (left operand type: "dtype[Any]", right
        # operand type: "Literal['M8[ns]']")
        if (
            isinstance(self.dtype, np.dtype)
            and isinstance(dtype, np.dtype)
            and dtype.kind == "M"
            and dtype != "M8[ns]"  # type: ignore[comparison-overlap]
        ):
            # For now Datetime supports this by unwrapping ndarray, but DTI doesn't
            raise TypeError(f"Cannot cast {type(self).__name__} to dtype")

        with rewrite_exception(type(self._data).__name__, type(self).__name__):
            new_values = self._data.astype(dtype, copy=copy)

        # pass copy=False because any copying will be done in the
        #  _data.astype call above
        return Index(new_values, dtype=new_values.dtype, name=self.name, copy=False)
