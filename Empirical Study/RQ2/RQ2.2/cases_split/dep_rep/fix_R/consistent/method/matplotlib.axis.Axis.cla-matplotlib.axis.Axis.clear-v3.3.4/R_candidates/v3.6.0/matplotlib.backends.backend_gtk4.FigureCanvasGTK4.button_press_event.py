    def button_press_event(self, controller, n_press, x, y):
        MouseEvent("button_press_event", self,
                   *self._mpl_coords((x, y)), controller.get_current_button()
                   )._process()
        self.grab_focus()
