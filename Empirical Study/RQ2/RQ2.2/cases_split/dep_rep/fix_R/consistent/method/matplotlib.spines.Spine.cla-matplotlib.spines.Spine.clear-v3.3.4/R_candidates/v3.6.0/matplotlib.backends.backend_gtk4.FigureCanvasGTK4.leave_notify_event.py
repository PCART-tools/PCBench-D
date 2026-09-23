    def leave_notify_event(self, controller):
        LocationEvent("figure_leave_event", self,
                      *self._mpl_coords())._process()
