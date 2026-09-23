    def __rmatmul__(self, other) -> DataFrame:
        """
        Matrix multiplication using binary `@` operator.
        """
        try:
            return self.T.dot(np.transpose(other)).T
        except ValueError as err:
            if "shape mismatch" not in str(err):
                raise
            # GH#21581 give exception message for original shapes
            msg = f"shapes {np.shape(other)} and {self.shape} not aligned"
            raise ValueError(msg) from err
