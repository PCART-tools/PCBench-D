    def _get_bbox_and_child_offsets(self, renderer):
        """
        Return the bbox of the offsetbox and the child offsets.

        The bbox should satisfy ``x0 <= x1 and y0 <= y1``.

        Parameters
        ----------
        renderer : `.RendererBase` subclass

        Returns
        -------
        bbox
        list of (xoffset, yoffset) pairs
        """
        raise NotImplementedError(
            "get_bbox_and_offsets must be overridden in derived classes")
