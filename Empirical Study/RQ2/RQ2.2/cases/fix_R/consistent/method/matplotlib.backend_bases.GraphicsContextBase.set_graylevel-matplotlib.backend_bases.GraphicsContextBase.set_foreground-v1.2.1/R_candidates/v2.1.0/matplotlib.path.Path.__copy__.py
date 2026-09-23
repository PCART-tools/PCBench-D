    def __copy__(self):
        """
        Returns a shallow copy of the `Path`, which will share the
        vertices and codes with the source `Path`.
        """
        import copy
        return copy.copy(self)
