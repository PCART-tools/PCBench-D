    def _invalidate_internal(self, value, invalidating_node):
        """
        Called by :meth:`invalidate` and subsequently ascends the transform
        stack calling each TransformNode's _invalidate_internal method.
        """
        # determine if this call will be an extension to the invalidation
        # status. If not, then a shortcut means that we needn't invoke an
        # invalidation up the transform stack as it will already have been
        # invalidated.

        # N.B This makes the invalidation sticky, once a transform has been
        # invalidated as NON_AFFINE, then it will always be invalidated as
        # NON_AFFINE even when triggered with a AFFINE_ONLY invalidation.
        # In most cases this is not a problem (i.e. for interactive panning and
        # zooming) and the only side effect will be on performance.
        status_changed = self._invalid < value

        if self.pass_through or status_changed:
            self._invalid = value

            for parent in list(self._parents.values()):
                # Dereference the weak reference
                parent = parent()
                if parent is not None:
                    parent._invalidate_internal(
                        value=value, invalidating_node=self)
