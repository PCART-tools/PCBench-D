    def __matmul__(self, other: AnyArrayLike | DataFrame) -> DataFrame | Series:
        """
        Matrix multiplication using binary `@` operator.
        """
        return self.dot(other)
