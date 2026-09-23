    def resizeEvent(self, event):
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
