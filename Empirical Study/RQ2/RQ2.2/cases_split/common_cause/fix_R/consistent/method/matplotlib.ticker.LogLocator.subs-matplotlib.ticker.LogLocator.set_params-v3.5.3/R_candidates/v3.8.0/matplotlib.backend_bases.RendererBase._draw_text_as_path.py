    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        """
        Draw the text by converting them to paths using `.TextToPath`.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        x : float
            The x location of the text in display coords.
        y : float
            The y location of the text baseline in display coords.
        s : str
            The text to be converted.
        prop : `~matplotlib.font_manager.FontProperties`
            The font property.
        angle : float
            Angle in degrees to render the text at.
        ismath : bool or "TeX"
            If True, use mathtext parser. If "TeX", use tex for rendering.
        """
        path, transform = self._get_text_path_transform(
            x, y, s, prop, angle, ismath)
        color = gc.get_rgb()
        gc.set_linewidth(0.0)
        self.draw_path(gc, path, transform, rgbFace=color)
