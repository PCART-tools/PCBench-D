    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw a text instance.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        x : float
            The x location of the text in display coords.
        y : float
            The y location of the text baseline in display coords.
        s : str
            The text string.
        prop : `~matplotlib.font_manager.FontProperties`
            The font properties.
        angle : float
            The rotation angle in degrees anti-clockwise.
        ismath : bool or "TeX"
            If True, use mathtext parser.
        mtext : `~matplotlib.text.Text`
            The original text object to be rendered.

        Notes
        -----
        **Notes for backend implementers:**

        `.RendererBase.draw_text` also supports passing "TeX" to the *ismath*
        parameter to use TeX rendering, but this is not required for actual
        rendering backends, and indeed many builtin backends do not support
        this.  Rather, TeX rendering is provided by `~.RendererBase.draw_tex`.
        """
        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath)
