    def __init__(self, figure, fh, dummy=False):
        """
        Creates a new PGF renderer that translates any drawing instruction
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

        # get LatexManager instance
        self.latexManager = LatexManagerFactory.get_latex_manager()

        if dummy:
            # dummy==True deactivate all methods
            nop = lambda *args, **kwargs: None
            for m in RendererPgf.__dict__:
                if m.startswith("draw_"):
                    self.__dict__[m] = nop
        else:
            # if fh does not belong to a filename, deactivate draw_image
            if not hasattr(fh, 'name') or not os.path.exists(fh.name):
                warnings.warn("streamed pgf-code does not support raster "
                              "graphics, consider using the pgf-to-pdf option",
                              UserWarning, stacklevel=2)
                self.__dict__["draw_image"] = lambda *args, **kwargs: None
