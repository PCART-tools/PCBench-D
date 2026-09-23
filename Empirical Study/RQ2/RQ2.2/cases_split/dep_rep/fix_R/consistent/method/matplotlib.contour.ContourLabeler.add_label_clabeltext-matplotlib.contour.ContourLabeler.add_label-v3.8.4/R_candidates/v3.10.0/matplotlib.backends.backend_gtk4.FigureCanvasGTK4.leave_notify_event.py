    def leave_notify_event(self, controller):
        LocationEvent(
            "figure_leave_event", self, *self._mpl_coords(),
            modifiers=self._mpl_modifiers(),
            guiEvent=controller.get_current_event(),
        )._process()
