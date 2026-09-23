    def _set_mathtext_path(self):
        """
        Draws mathtext markers '$...$' using TextPath object.

        Submitted by tcb
        """
        from matplotlib.text import TextPath
        from matplotlib.font_manager import FontProperties

        # again, the properties could be initialised just once outside
        # this function
        # Font size is irrelevant here, it will be rescaled based on
        # the drawn size later
        props = FontProperties(size=1.0)
        text = TextPath(xy=(0, 0), s=self.get_marker(), fontproperties=props,
                        usetex=rcParams['text.usetex'])
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
