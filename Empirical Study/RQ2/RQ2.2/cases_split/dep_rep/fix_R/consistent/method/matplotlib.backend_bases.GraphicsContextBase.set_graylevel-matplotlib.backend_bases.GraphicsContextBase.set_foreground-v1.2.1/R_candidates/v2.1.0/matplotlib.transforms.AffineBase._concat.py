    @staticmethod
    def _concat(a, b):
        """
        Concatenates two transformation matrices (represented as numpy
        arrays) together.
        """
        return np.dot(b, a)
