    @classmethod
    def get_grey(cls, tex, fontsize=None, dpi=None):
        """Return the alpha channel."""
        if not fontsize:
            fontsize = mpl.rcParams['font.size']
        if not dpi:
            dpi = mpl.rcParams['savefig.dpi']
        key = cls._get_tex_source(tex, fontsize), dpi
        alpha = cls._grey_arrayd.get(key)
        if alpha is None:
            pngfile = cls.make_png(tex, fontsize, dpi)
            rgba = mpl.image.imread(os.path.join(cls._texcache, pngfile))
            cls._grey_arrayd[key] = alpha = rgba[:, :, -1]
        return alpha
