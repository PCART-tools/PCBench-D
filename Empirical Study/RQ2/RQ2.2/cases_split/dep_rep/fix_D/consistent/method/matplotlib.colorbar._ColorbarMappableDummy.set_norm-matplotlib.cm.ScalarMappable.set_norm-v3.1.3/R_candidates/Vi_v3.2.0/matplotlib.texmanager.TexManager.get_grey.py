    def get_grey(self, tex, fontsize=None, dpi=None):
        """Return the alpha channel."""
        from matplotlib import _png
        key = tex, self.get_font_config(), fontsize, dpi
        alpha = self.grey_arrayd.get(key)
        if alpha is None:
            pngfile = self.make_png(tex, fontsize, dpi)
            with open(os.path.join(self.texcache, pngfile), "rb") as file:
                X = _png.read_png(file)
            self.grey_arrayd[key] = alpha = X[:, :, -1]
        return alpha
