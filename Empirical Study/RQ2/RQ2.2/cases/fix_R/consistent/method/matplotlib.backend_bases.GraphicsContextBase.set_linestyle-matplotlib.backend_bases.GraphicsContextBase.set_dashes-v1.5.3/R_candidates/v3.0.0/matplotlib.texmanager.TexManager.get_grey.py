    def get_grey(self, tex, fontsize=None, dpi=None):
        """Return the alpha channel."""
        key = tex, self.get_font_config(), fontsize, dpi
        alpha = self.grey_arrayd.get(key)
        if alpha is None:
            pngfile = self.make_png(tex, fontsize, dpi)
            X = _png.read_png(os.path.join(self.texcache, pngfile))
            self.grey_arrayd[key] = alpha = X[:, :, -1]
        return alpha
