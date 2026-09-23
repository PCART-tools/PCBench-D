    def enter_notify_event(self, controller, x, y):
        LocationEvent("figure_enter_event", self,
                      *self._mpl_coords((x, y)))._process()
