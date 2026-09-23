    def button_release_event(self, controller, n_press, x, y):
        MouseEvent("button_release_event", self,
                   *self._mpl_coords((x, y)), controller.get_current_button()
                   )._process()
