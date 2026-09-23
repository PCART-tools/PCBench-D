    def enter_notify_event(self, widget, event):
        x, y, state = event.window.get_pointer()
        FigureCanvasBase.enter_notify_event(self, event, xy=(x, y))
