    def __call__(self):
        """
        Return a list of the registered colormap names.

        This exists only for backward-compatibilty in `.pyplot` which had a
        ``plt.colormaps()`` method. The recommended way to get this list is
        now ``list(colormaps)``.
        """
        return list(self)
