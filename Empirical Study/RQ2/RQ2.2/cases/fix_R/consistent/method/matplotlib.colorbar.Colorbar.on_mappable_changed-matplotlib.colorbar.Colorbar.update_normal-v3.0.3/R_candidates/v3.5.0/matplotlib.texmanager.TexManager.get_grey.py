    def get_grey(self, tex, fontsize=None, dpi=None):
        """Return the alpha channel."""
        if not fontsize:
            fontsize = rcParams['font.size']
        if not dpi:
            dpi = rcParams['savefig.dpi']
        key = tex, self.get_font_config(), fontsize, dpi
        alpha = self._grey_arrayd.get(key)
        if alpha is None:
            pngfile = self.make_png(tex, fontsize, dpi)
            rgba = mpl.image.imread(os.path.join(self.texcache, pngfile))
            self._grey_arrayd[key] = alpha = rgba[:, :, -1]
        return alpha
