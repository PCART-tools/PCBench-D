    def get_patch_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` instance which
        takes patch coordinates to data coordinates.

        For example, one may define a patch of a circle which represents a
        radius of 5 by providing coordinates for a unit circle, and a
        transform which scales the coordinates (the patch coordinate) by 5.
        """
        return transforms.IdentityTransform()
