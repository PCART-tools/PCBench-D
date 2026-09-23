    @cbook._delete_parameter("3.3", "dummy")
    def __init__(self, figure, fh, dummy=False):
        """
        Create a new PGF renderer that translates any drawing instruction
        into text commands to be interpreted in a latex pgfpicture environment.

        Attributes
        ----------
        figure : `matplotlib.figure.Figure`
            Matplotlib figure to initialize height, width and dpi from.
        fh : file-like
            File handle for the output of the drawing commands.
        """

        RendererBase.__init__(self)
        self.dpi = figure.dpi
        self.fh = fh
        self.figure = figure
        self.image_counter = 0

        self._latexManager = LatexManager._get_cached_or_new()  # deprecated

        if dummy:
            # dummy==True deactivate all methods
            for m in RendererPgf.__dict__:
                if m.startswith("draw_"):
                    self.__dict__[m] = lambda *args, **kwargs: None
