    @_allow_super_init
    def __init__(self, figure):
        _create_qApp()
        figure._original_dpi = figure.dpi

        super(FigureCanvasQT, self).__init__(figure=figure)

        self.figure = figure
        self._update_figure_dpi()

        w, h = self.get_width_height()
        self.resize(w, h)

        self.setMouseTracking(True)
        # Key auto-repeat enabled by default
        self._keyautorepeat = True

        # In cases with mixed resolution displays, we need to be careful if the
        # dpi_ratio changes - in this case we need to resize the canvas
        # accordingly. We could watch for screenChanged events from Qt, but
        # the issue is that we can't guarantee this will be emitted *before*
        # the first paintEvent for the canvas, so instead we keep track of the
        # dpi_ratio value here and in paintEvent we resize the canvas if
        # needed.
        self._dpi_ratio_prev = None
