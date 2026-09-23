    def inverse(self, value):
        """
        Raises
        ------
        ValueError
            BoundaryNorm is not invertible, so calling this method will always
            raise an error
        """
        return ValueError("BoundaryNorm is not invertible")
