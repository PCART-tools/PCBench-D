    def get_rgba(self, tex, fontsize=None, dpi=None, rgb=(0, 0, 0)):
        """
        Returns latex's rendering of the tex string as an rgba array
        """
        if not fontsize:
            fontsize = rcParams['font.size']
        if not dpi:
            dpi = rcParams['savefig.dpi']
        r, g, b = rgb
        key = tex, self.get_font_config(), fontsize, dpi, tuple(rgb)
        Z = self.rgba_arrayd.get(key)

        if Z is None:
            alpha = self.get_grey(tex, fontsize, dpi)

            Z = np.zeros((alpha.shape[0], alpha.shape[1], 4), float)

            Z[:, :, 0] = r
            Z[:, :, 1] = g
            Z[:, :, 2] = b
            Z[:, :, 3] = alpha
            self.rgba_arrayd[key] = Z

        return Z
