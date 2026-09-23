    def _set_mathtext_path(self):
        """
        Draw mathtext markers '$...$' using `.TextPath` object.

        Submitted by tcb
        """
        from matplotlib.text import TextPath

        # again, the properties could be initialised just once outside
        # this function
        text = TextPath(xy=(0, 0), s=self.get_marker(),
                        usetex=mpl.rcParams['text.usetex'])
        if len(text.vertices) == 0:
            return

        bbox = text.get_extents()
        max_dim = max(bbox.width, bbox.height)
        self._transform = (
            Affine2D()
            .translate(-bbox.xmin + 0.5 * -bbox.width, -bbox.ymin + 0.5 * -bbox.height)
            .scale(1.0 / max_dim))
        self._path = text
        self._snap = False
