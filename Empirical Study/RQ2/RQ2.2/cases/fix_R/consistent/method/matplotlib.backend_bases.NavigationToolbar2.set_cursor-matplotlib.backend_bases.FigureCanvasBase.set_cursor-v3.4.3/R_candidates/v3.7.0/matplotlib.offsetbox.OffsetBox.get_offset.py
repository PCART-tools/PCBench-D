    @_compat_get_offset
    def get_offset(self, bbox, renderer):
        """
        Return the offset as a tuple (x, y).

        The extent parameters have to be provided to handle the case where the
        offset is dynamically determined by a callable (see
        `~.OffsetBox.set_offset`).

        Parameters
        ----------
        bbox : `.Bbox`
        renderer : `.RendererBase` subclass
        """
        return (
            self._offset(bbox.width, bbox.height, -bbox.x0, -bbox.y0, renderer)
            if callable(self._offset)
            else self._offset)
