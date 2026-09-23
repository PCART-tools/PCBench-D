    def get_transform(self):
        """Return the `.Transform` instance used by this artist."""
        if self._transform is None:
            self._transform = IdentityTransform()
        elif (not isinstance(self._transform, Transform)
              and hasattr(self._transform, '_as_mpl_transform')):
            self._transform = self._transform._as_mpl_transform(self.axes)
        return self._transform
