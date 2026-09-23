    def get_transform(self):
        """
        Return the `~matplotlib.transforms.Transform` applied to the children.
        """
        return self.dpi_transform + self.offset_transform
