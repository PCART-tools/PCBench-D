    def _wrap_joined_index(
        self,
        joined: ArrayLike,
        other: Self,
        lidx: npt.NDArray[np.intp],
        ridx: npt.NDArray[np.intp],
    ) -> Self:
        assert other.dtype == self.dtype

        if isinstance(self, ABCMultiIndex):
            name = self.names if self.names == other.names else None
            # error: Incompatible return value type (got "MultiIndex",
            # expected "Self")
            mask = lidx == -1
            join_idx = self.take(lidx)
            right = other.take(ridx)
            join_index = join_idx.putmask(mask, right)._sort_levels_monotonic()
            return join_index.set_names(name)  # type: ignore[return-value]
        else:
            name = get_op_result_name(self, other)
            return self._constructor._with_infer(joined, name=name, dtype=self.dtype)
