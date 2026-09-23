    def resizeEvent(self, event):
        # _dpi_ratio_prev will be set the first time the canvas is painted, and
        # the rendered buffer is useless before anyways.
        if self._dpi_ratio_prev is None:
            return
        w = event.size().width() * self._dpi_ratio
        h = event.size().height() * self._dpi_ratio
        dpival = self.figure.dpi
        winch = w / dpival
        hinch = h / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        # pass back into Qt to let it finish
        QtWidgets.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)
