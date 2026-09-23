    def set(self, child):
        """
        Replace the current child of this transform with another one.

        The new child must have the same number of input and output
        dimensions as the current child.
        """
        if (child.input_dims != self.input_dims or
                child.output_dims != self.output_dims):
            raise ValueError(
                "The new child must have the same number of input and output "
                "dimensions as the current child")

        self.set_children(child)
        self._set(child)

        self._invalid = 0
        self.invalidate()
        self._invalid = 0
