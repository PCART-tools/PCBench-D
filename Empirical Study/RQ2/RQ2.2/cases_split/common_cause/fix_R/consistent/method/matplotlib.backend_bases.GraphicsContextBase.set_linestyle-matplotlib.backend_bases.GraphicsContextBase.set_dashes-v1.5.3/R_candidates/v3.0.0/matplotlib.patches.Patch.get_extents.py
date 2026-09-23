    def get_extents(self):
        """
        Return a :class:`~matplotlib.transforms.Bbox` object defining
        the axis-aligned extents of the :class:`Patch`.
        """
        return self.get_path().get_extents(self.get_transform())
