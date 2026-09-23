    def set(self, child):
        """
        Replace the current child of this transform with another one.

        The new child must have the same number of input and output
        dimensions as the current child.
        """
        if hasattr(self, "_child"):  # Absent during init.
            self.invalidate()
            new_dims = (child.input_dims, child.output_dims)
            old_dims = (self._child.input_dims, self._child.output_dims)
            if new_dims != old_dims:
                raise ValueError(
                    f"The input and output dims of the new child {new_dims} "
                    f"do not match those of current child {old_dims}")
            self._child._parents.pop(id(self), None)

        self._child = child
        self.set_children(child)

        self.transform = child.transform
        self.transform_affine = child.transform_affine
        self.transform_non_affine = child.transform_non_affine
        self.transform_path = child.transform_path
        self.transform_path_affine = child.transform_path_affine
        self.transform_path_non_affine = child.transform_path_non_affine
        self.get_affine = child.get_affine
        self.inverted = child.inverted
        self.get_matrix = child.get_matrix
        # note we do not wrap other properties here since the transform's
        # child can be changed with WrappedTransform.set and so checking
        # is_affine and other such properties may be dangerous.

        self._invalid = 0
        self.invalidate()
        self._invalid = 0
