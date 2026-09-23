    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        """
        Draw the text by converting them to paths using textpath module.

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
            The font property.
        s : str
            The text to be converted.
        usetex : bool
            Whether to use usetex mode.
        ismath : bool or "TeX"
            If True, use mathtext parser. If "TeX", use *usetex* mode.
        """
        path, transform = self._get_text_path_transform(
            x, y, s, prop, angle, ismath)
        color = gc.get_rgb()
        gc.set_linewidth(0.0)
        self.draw_path(gc, path, transform, rgbFace=color)
