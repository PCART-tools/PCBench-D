    def resizeEvent(self, event):
        frame = sys._getframe()
        # Prevent PyQt6 recursion, but sometimes frame.f_back is None
        if frame.f_code is getattr(frame.f_back, 'f_code', None):
            return
        w = event.size().width() * self.device_pixel_ratio
        h = event.size().height() * self.device_pixel_ratio

        dpival = self.figure.dpi
        winch = w / dpival
        hinch = h / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        # pass back into Qt to let it finish
        QtWidgets.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)
