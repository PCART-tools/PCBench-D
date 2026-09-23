    def _unit_change_handler(self, axis_name, event=None):
        """
        Process axis units changes: requests updates to data and view limits.
        """
        if event is None:  # Allow connecting `self._unit_change_handler(name)`
            return functools.partial(
                self._unit_change_handler, axis_name, event=object())
        _api.check_in_list(self._get_axis_map(), axis_name=axis_name)
        for line in self.lines:
            line.recache_always()
        self.relim()
        self._request_autoscale_view(scalex=(axis_name == "x"),
                                     scaley=(axis_name == "y"))
