    def __rmatmul__(self, other):
        """
        Matrix multiplication using binary `@` operator.
        """
        return self.dot(np.transpose(other))
