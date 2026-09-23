    def get_extent_offsets(self, renderer):
        """
        Update offset of the children and return the extent of the box.

        Parameters
        ----------
        renderer : `.RendererBase` subclass

        Returns
        -------
        width
        height
        xdescent
        ydescent
        list of (xoffset, yoffset) pairs
        """
        raise NotImplementedError(
            "get_extent_offsets must be overridden in derived classes.")
