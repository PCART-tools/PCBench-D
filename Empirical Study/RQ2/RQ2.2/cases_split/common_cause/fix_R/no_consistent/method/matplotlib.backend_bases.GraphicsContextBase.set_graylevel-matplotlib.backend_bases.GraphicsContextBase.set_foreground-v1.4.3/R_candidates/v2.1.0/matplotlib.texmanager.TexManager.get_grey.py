    def get_grey(self, tex, fontsize=None, dpi=None):
        """returns the alpha channel"""
        key = tex, self.get_font_config(), fontsize, dpi
        alpha = self.grey_arrayd.get(key)
        if alpha is None:
            pngfile = self.make_png(tex, fontsize, dpi)
            X = read_png(os.path.join(self.texcache, pngfile))
            self.grey_arrayd[key] = alpha = X[:, :, -1]
        return alpha
