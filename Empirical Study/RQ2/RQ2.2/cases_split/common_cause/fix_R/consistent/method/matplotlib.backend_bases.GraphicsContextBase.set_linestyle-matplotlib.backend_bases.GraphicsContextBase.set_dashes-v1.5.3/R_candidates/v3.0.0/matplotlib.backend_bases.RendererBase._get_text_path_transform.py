    def _get_text_path_transform(self, x, y, s, prop, angle, ismath):
        """
        return the text path and transform

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
          font property

        s : str
          text to be converted

        usetex : bool
          If True, use matplotlib usetex mode.

        ismath : bool
          If True, use mathtext parser. If "TeX", use *usetex* mode.
        """

        text2path = self._text2path
        fontsize = self.points_to_pixels(prop.get_size_in_points())

        if ismath == "TeX":
            verts, codes = text2path.get_text_path(prop, s, ismath=False,
                                                   usetex=True)
        else:
            verts, codes = text2path.get_text_path(prop, s, ismath=ismath,
                                                   usetex=False)

        path = Path(verts, codes)
        angle = np.deg2rad(angle)
        if self.flipy():
            transform = Affine2D().scale(fontsize / text2path.FONT_SCALE,
                                         fontsize / text2path.FONT_SCALE)
            transform = transform.rotate(angle).translate(x, self.height - y)
        else:
            transform = Affine2D().scale(fontsize / text2path.FONT_SCALE,
                                         fontsize / text2path.FONT_SCALE)
            transform = transform.rotate(angle).translate(x, y)

        return path, transform
