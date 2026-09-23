    def _set_mathtext_path(self):
        """
        Draw mathtext markers '$...$' using TextPath object.

        Submitted by tcb
        """
        from matplotlib.textpath import TextPath

        # again, the properties could be initialised just once outside
        # this function
        text = TextPath(xy=(0, 0), s=self.get_marker(),
                        usetex=mpl.rcParams['text.usetex'])
        if len(text.vertices) == 0:
            return

        xmin, ymin = text.vertices.min(axis=0)
        xmax, ymax = text.vertices.max(axis=0)
        width = xmax - xmin
        height = ymax - ymin
        max_dim = max(width, height)
        self._transform = Affine2D() \
            .translate(-xmin + 0.5 * -width, -ymin + 0.5 * -height) \
            .scale(1.0 / max_dim)
        self._path = text
        self._snap = False
