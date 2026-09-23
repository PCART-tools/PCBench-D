    def __init__(self, figure):
        FigureCanvasBase.__init__(self, figure)
        if self.__class__ == matplotlib.backends.backend_gdk.FigureCanvasGDK:
            warn_deprecated('2.0', message="The GDK backend is "
                            "deprecated. It is untested, known to be "
                            "broken and will be removed in Matplotlib 2.2. "
                            "Use the Agg backend instead. "
                            "See Matplotlib usage FAQ for"
                            " more info on backends.",
                            alternative="Agg")
        self._renderer_init()
