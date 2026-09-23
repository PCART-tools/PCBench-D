    def button_release_event(self, widget, event):
        MouseEvent("button_release_event", self,
                   *self._mpl_coords(event), event.button,
                   guiEvent=event)._process()
        return False  # finish event propagation?
