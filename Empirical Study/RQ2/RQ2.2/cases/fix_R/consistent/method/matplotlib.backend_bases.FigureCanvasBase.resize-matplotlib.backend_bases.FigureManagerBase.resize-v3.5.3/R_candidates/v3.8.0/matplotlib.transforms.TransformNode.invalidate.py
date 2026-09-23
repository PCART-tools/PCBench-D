    def invalidate(self):
        """
        Invalidate this `TransformNode` and triggers an invalidation of its
        ancestors.  Should be called any time the transform changes.
        """
        return self._invalidate_internal(
            level=self._INVALID_AFFINE_ONLY if self.is_affine else self._INVALID_FULL,
            invalidating_node=self)
