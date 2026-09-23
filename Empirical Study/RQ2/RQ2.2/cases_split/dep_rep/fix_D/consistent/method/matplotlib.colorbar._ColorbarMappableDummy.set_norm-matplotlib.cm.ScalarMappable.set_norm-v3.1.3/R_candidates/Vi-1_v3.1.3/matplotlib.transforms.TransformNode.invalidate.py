    def invalidate(self):
        """
        Invalidate this :class:`TransformNode` and triggers an
        invalidation of its ancestors.  Should be called any
        time the transform changes.
        """
        value = self.INVALID
        if self.is_affine:
            value = self.INVALID_AFFINE
        return self._invalidate_internal(value, invalidating_node=self)
