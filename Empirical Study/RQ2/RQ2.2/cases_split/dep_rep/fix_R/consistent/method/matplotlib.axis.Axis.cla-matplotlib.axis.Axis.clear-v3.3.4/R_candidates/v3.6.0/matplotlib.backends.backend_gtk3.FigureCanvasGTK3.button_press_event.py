    def button_press_event(self, widget, event):
        MouseEvent("button_press_event", self,
                   *self._mpl_coords(event), event.button,
                   guiEvent=event)._process()
        return False  # finish event propagation?
