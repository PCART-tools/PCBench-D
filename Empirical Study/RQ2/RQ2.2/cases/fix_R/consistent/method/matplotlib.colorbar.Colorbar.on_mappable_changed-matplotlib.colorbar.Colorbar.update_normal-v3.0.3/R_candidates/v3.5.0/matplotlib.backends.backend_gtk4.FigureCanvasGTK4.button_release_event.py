    def button_release_event(self, controller, n_press, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.button_release_event(self, x, y,
                                              controller.get_current_button())
