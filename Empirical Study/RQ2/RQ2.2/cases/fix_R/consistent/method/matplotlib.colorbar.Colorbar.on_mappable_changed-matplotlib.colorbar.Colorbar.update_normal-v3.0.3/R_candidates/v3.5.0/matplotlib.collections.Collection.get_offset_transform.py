    def get_offset_transform(self):
        """Return the `.Transform` instance used by this artist offset."""
        if self._transOffset is None:
            self._transOffset = transforms.IdentityTransform()
        elif (not isinstance(self._transOffset, transforms.Transform)
              and hasattr(self._transOffset, '_as_mpl_transform')):
            self._transOffset = self._transOffset._as_mpl_transform(self.axes)
        return self._transOffset
