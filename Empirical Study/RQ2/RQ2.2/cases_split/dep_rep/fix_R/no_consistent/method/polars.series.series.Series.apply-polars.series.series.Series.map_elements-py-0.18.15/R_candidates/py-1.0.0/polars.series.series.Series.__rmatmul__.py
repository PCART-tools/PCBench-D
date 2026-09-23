    def __rmatmul__(self, other: Any) -> float | Series | None:
        if isinstance(other, Sequence) or (
            _check_for_numpy(other) and isinstance(other, np.ndarray)
        ):
            other = Series(other)
        return other.dot(self)
