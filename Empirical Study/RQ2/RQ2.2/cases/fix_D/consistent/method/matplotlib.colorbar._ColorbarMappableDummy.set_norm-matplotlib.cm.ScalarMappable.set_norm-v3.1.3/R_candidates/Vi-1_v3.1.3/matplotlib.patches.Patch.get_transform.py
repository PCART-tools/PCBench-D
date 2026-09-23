    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` applied
        to the :class:`Patch`.
        """
        return self.get_patch_transform() + artist.Artist.get_transform(self)
