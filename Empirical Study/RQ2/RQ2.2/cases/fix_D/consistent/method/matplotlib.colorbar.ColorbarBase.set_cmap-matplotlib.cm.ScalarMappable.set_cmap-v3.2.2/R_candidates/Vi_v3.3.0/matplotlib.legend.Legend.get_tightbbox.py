    def get_tightbbox(self, renderer):
        """
        Like `.Legend.get_window_extent`, but uses the box for the legend.

        Parameters
        ----------
        renderer : `.RendererBase` subclass
            renderer that will be used to draw the figures (i.e.
            ``fig.canvas.get_renderer()``)

        Returns
        -------
        `.BboxBase`
            The bounding box in figure pixel coordinates.
        """
        return self._legend_box.get_window_extent(renderer)
