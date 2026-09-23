    def _invalidate_internal(self, level, invalidating_node):
        """
        Called by :meth:`invalidate` and subsequently ascends the transform
        stack calling each TransformNode's _invalidate_internal method.
        """
        # If we are already more invalid than the currently propagated invalidation,
        # then we don't need to do anything.
        if level <= self._invalid and not self.pass_through:
            return
        self._invalid = level
        for parent in list(self._parents.values()):
            parent = parent()  # Dereference the weak reference.
            if parent is not None:
                parent._invalidate_internal(level=level, invalidating_node=self)
