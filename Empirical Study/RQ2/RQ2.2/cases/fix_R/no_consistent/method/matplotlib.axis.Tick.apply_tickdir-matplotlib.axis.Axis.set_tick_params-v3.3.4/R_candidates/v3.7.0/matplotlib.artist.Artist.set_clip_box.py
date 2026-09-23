    def set_clip_box(self, clipbox):
        """
        Set the artist's clip `.Bbox`.

        Parameters
        ----------
        clipbox : `.Bbox`

            Typically would be created from a `.TransformedBbox`. For
            instance ``TransformedBbox(Bbox([[0, 0], [1, 1]]), ax.transAxes)``
            is the default clipping for an artist added to an Axes.

        """
        self.clipbox = clipbox
        self.pchanged()
        self.stale = True
