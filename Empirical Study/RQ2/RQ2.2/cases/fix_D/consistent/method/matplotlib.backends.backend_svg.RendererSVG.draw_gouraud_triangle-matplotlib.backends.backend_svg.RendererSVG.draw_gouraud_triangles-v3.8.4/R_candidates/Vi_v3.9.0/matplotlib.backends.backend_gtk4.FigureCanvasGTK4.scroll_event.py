    def scroll_event(self, controller, dx, dy):
        MouseEvent(
            "scroll_event", self, *self._mpl_coords(), step=dy,
            modifiers=self._mpl_modifiers(controller),
        )._process()
        return True
