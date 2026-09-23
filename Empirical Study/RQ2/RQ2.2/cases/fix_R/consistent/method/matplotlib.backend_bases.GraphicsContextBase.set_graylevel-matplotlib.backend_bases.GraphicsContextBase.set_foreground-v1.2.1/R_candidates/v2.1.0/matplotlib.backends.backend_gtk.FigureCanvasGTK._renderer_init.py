    def _renderer_init(self):
        """Override by GTK backends to select a different renderer
        Renderer should provide the methods:
            set_pixmap ()
            set_width_height ()
        that are used by
            _render_figure() / _pixmap_prepare()
        """
        self._renderer = RendererGDK (self, self.figure.dpi)
