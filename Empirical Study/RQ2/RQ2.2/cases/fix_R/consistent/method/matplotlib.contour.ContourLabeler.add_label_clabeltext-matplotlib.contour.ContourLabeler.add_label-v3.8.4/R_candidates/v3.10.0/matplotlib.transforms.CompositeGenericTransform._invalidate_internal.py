    def _invalidate_internal(self, level, invalidating_node):
        # When the left child is invalidated at AFFINE_ONLY level and the right child is
        # non-affine, the composite transform is FULLY invalidated.
        if invalidating_node is self._a and not self._b.is_affine:
            level = Transform._INVALID_FULL
        super()._invalidate_internal(level, invalidating_node)
