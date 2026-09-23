    def __matmul__(
        self, other: AnyArrayLike | DataFrame | Series
    ) -> DataFrame | Series:
        """
        Matrix multiplication using binary `@` operator in Python>=3.5.
        """
        return self.dot(other)
