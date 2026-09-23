    def enter_notify_event(self, controller, x, y):
        LocationEvent(
            "figure_enter_event", self, *self._mpl_coords((x, y)),
            modifiers=self._mpl_modifiers(),
            guiEvent=controller.get_current_event(),
        )._process()
