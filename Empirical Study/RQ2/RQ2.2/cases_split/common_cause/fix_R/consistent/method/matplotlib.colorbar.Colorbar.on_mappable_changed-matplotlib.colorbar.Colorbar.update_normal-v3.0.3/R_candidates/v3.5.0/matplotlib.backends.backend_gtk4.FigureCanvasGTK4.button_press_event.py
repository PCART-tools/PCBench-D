    def button_press_event(self, controller, n_press, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.button_press_event(self, x, y,
                                            controller.get_current_button())
        self.grab_focus()
