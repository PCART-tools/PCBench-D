    @_allow_super_init
    def __init__(self, figure=None):
        _create_qApp()
        super().__init__(figure=figure)

        # We don't want to scale up the figure DPI more than once.
        # Note, we don't handle a signal for changing DPI yet.
        self.figure._original_dpi = self.figure.dpi
        self._update_figure_dpi()
        # In cases with mixed resolution displays, we need to be careful if the
        # dpi_ratio changes - in this case we need to resize the canvas
        # accordingly.
        self._dpi_ratio_prev = self._dpi_ratio

        self._draw_pending = False
        self._is_drawing = False
        self._draw_rect_callback = lambda painter: None

        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.resize(*self.get_width_height())

        palette = QtGui.QPalette(QtCore.Qt.white)
        self.setPalette(palette)
