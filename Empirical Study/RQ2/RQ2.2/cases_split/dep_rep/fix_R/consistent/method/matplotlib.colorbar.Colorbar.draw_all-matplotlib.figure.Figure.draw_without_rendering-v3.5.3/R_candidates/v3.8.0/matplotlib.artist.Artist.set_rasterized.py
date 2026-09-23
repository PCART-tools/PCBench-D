    def set_rasterized(self, rasterized):
        """
        Force rasterized (bitmap) drawing for vector graphics output.

        Rasterized drawing is not supported by all artists. If you try to
        enable this on an artist that does not support it, the command has no
        effect and a warning will be issued.

        This setting is ignored for pixel-based output.

        See also :doc:`/gallery/misc/rasterization_demo`.

        Parameters
        ----------
        rasterized : bool
        """
        supports_rasterization = getattr(self.draw,
                                         "_supports_rasterization", False)
        if rasterized and not supports_rasterization:
            _api.warn_external(f"Rasterization of '{self}' will be ignored")

        self._rasterized = rasterized
