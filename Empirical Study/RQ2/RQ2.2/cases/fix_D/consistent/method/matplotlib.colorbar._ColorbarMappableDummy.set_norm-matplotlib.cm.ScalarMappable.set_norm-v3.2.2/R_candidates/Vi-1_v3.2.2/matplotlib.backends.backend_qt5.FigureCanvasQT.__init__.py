    @_allow_super_init
    def __init__(self, figure):
        _create_qApp()
        super().__init__(figure=figure)

        self.figure = figure
        # We don't want to scale up the figure DPI more than once.
        # Note, we don't handle a signal for changing DPI yet.
        figure._original_dpi = figure.dpi
        self._update_figure_dpi()
        # In cases with mixed resolution displays, we need to be careful if the
        # dpi_ratio changes - in this case we need to resize the canvas
        # accordingly. We could watch for screenChanged events from Qt, but
        # the issue is that we can't guarantee this will be emitted *before*
        # the first paintEvent for the canvas, so instead we keep track of the
        # dpi_ratio value here and in paintEvent we resize the canvas if
        # needed.
        self._dpi_ratio_prev = None

        self._draw_pending = False
        self._is_drawing = False
        self._draw_rect_callback = lambda painter: None

        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.resize(*self.get_width_height())

        palette = QtGui.QPalette(QtCore.Qt.white)
        self.setPalette(palette)
