    def get_data_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` instance which
        maps data coordinates to physical coordinates.
        """
        return artist.Artist.get_transform(self)
