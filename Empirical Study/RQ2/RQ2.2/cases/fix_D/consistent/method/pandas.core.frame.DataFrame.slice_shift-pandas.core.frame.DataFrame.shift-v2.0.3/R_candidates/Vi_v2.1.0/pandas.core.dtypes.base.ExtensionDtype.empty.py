    def empty(self, shape: Shape) -> ExtensionArray:
        """
        Construct an ExtensionArray of this dtype with the given shape.

        Analogous to numpy.empty.

        Parameters
        ----------
        shape : int or tuple[int]

        Returns
        -------
        ExtensionArray
        """
        cls = self.construct_array_type()
        return cls._empty(shape, dtype=self)
