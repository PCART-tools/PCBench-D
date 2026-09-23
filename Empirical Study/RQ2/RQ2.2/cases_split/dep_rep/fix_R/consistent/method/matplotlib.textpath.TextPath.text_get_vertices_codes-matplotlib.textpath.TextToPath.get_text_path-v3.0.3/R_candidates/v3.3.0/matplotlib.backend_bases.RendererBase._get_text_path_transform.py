    def _get_text_path_transform(self, x, y, s, prop, angle, ismath):
        """
        Return the text path and transform.

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
            The font property.
        s : str
            The text to be converted.
        ismath : bool or "TeX"
            If True, use mathtext parser. If "TeX", use *usetex* mode.
        """

        text2path = self._text2path
        fontsize = self.points_to_pixels(prop.get_size_in_points())
        verts, codes = text2path.get_text_path(prop, s, ismath=ismath)

        path = Path(verts, codes)
        angle = np.deg2rad(angle)
        if self.flipy():
            width, height = self.get_canvas_width_height()
            transform = (Affine2D()
                         .scale(fontsize / text2path.FONT_SCALE)
                         .rotate(angle)
                         .translate(x, height - y))
        else:
            transform = (Affine2D()
                         .scale(fontsize / text2path.FONT_SCALE)
                         .rotate(angle)
                         .translate(x, y))

        return path, transform
