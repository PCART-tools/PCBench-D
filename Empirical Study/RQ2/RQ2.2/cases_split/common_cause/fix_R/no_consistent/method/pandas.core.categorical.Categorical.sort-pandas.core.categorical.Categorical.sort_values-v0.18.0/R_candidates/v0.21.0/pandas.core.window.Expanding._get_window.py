    def _get_window(self, other=None):
        obj = self._selected_obj
        if other is None:
            return (max(len(obj), self.min_periods) if self.min_periods
                    else len(obj))
        return (max((len(obj) + len(obj)), self.min_periods)
                if self.min_periods else (len(obj) + len(obj)))
