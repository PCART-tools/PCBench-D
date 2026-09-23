    def get_rgba(self, tex, fontsize=None, dpi=None, rgb=(0, 0, 0)):
        """Return latex's rendering of the tex string as an rgba array."""
        alpha = self.get_grey(tex, fontsize, dpi)
        rgba = np.empty((*alpha.shape, 4))
        rgba[..., :3] = mpl.colors.to_rgb(rgb)
        rgba[..., -1] = alpha
        return rgba
