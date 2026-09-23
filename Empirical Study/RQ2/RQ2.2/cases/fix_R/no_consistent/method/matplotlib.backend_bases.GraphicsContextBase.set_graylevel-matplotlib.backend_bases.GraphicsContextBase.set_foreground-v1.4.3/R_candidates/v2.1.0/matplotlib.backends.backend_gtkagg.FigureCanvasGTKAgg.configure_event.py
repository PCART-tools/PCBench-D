    def configure_event(self, widget, event=None):

        if DEBUG: print('FigureCanvasGTKAgg.configure_event')
        if widget.window is None:
            return
        try:
            del self.renderer
        except AttributeError:
            pass
        w,h = widget.window.get_size()
        if w==1 or h==1: return # empty fig

        # compute desired figure size in inches
        dpival = self.figure.dpi
        winch = w/dpival
        hinch = h/dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        self._need_redraw = True
        self.resize_event()
        if DEBUG: print('FigureCanvasGTKAgg.configure_event end')
        return True
