    def can_composite(self):
        """
        Returns `True` if the image can be composited with its neighbors.
        """
        trans = self.get_transform()
        return (
            self._interpolation != 'none' and
            trans.is_affine and
            trans.is_separable)
