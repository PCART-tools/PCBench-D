    def get_kern(self, font1, fontclass1, sym1, fontsize1,
                 font2, fontclass2, sym2, fontsize2, dpi):
        r"""
        Get the kerning distance for font between *sym1* and *sym2*.

        *fontX*: one of the TeX font names::

          tt, it, rm, cal, sf, bf or default/regular (non-math)

        *fontclassX*: TODO

        *symX*: a symbol in raw TeX form. e.g., '1', 'x' or '\sigma'

        *fontsizeX*: the fontsize in points

        *dpi*: the current dots-per-inch
        """
        return 0.
