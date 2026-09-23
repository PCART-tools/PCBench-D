    def size_allocate(self, widget, allocation):
        dpival = self.figure.dpi
        winch = allocation.width / dpival
        hinch = allocation.height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        FigureCanvasBase.resize_event(self)
        self.draw_idle()
