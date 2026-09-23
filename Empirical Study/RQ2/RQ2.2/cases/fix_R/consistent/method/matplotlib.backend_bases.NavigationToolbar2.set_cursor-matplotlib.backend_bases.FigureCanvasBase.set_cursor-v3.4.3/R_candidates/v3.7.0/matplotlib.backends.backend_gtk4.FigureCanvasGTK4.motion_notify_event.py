    def motion_notify_event(self, controller, x, y):
        MouseEvent(
            "motion_notify_event", self, *self._mpl_coords((x, y)),
            modifiers=self._mpl_modifiers(controller),
        )._process()
