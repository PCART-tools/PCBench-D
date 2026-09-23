    def __init__(self, gtkDA, dpi):
        # widget gtkDA is used for:
        #  '<widget>.create_pango_layout(s)'
        #  cmap line below)
        self.gtkDA = gtkDA
        self.dpi   = dpi
        self._cmap = gtkDA.get_colormap()
        self.mathtext_parser = MathTextParser("Agg")
