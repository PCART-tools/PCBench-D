    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        """
        Draw a TeX instance.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        x : float
            The x location of the text in display coords.
        y : float
            The y location of the text baseline in display coords.
        s : str
            The TeX text string.
        prop : `~matplotlib.font_manager.FontProperties`
            The font properties.
        angle : float
            The rotation angle in degrees anti-clockwise.
        mtext : `~matplotlib.text.Text`
            The original text object to be rendered.
        """
        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath="TeX")
