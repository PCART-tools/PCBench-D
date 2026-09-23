    def motion_notify_event(self, controller, x, y):
        MouseEvent(
            "motion_notify_event", self, *self._mpl_coords((x, y)),
            buttons=self._mpl_buttons(controller),
            modifiers=self._mpl_modifiers(controller),
            guiEvent=controller.get_current_event(),
        )._process()
