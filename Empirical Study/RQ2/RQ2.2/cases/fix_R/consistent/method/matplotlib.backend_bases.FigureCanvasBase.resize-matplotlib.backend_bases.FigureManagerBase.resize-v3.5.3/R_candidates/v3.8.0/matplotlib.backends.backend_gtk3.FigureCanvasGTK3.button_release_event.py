    def button_release_event(self, widget, event):
        MouseEvent("button_release_event", self,
                   *self._mpl_coords(event), event.button,
                   modifiers=self._mpl_modifiers(event.state),
                   guiEvent=event)._process()
        return False  # finish event propagation?
