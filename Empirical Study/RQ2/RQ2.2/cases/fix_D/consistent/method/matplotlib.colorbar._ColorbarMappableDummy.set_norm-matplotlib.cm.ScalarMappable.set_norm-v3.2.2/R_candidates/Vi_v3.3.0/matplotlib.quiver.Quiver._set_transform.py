    def _set_transform(self):
        """
        Set the PolyCollection transform to go
        from arrow width units to pixels.
        """
        dx = self._dots_per_unit(self.units)
        self._trans_scale = dx  # pixels per arrow width unit
        trans = transforms.Affine2D().scale(dx)
        self.set_transform(trans)
        return trans
