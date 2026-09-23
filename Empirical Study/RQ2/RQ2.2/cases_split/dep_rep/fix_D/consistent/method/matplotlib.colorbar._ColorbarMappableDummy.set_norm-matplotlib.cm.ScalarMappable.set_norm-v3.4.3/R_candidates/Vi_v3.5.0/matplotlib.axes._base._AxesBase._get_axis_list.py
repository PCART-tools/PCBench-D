    def _get_axis_list(self):
        return tuple(getattr(self, f"{name}axis") for name in self._axis_names)
