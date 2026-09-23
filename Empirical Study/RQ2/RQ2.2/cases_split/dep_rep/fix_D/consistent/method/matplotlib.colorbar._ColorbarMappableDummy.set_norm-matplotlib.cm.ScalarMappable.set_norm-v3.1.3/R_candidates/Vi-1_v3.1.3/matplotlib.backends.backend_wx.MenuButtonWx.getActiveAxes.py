    def getActiveAxes(self):
        """Return a list of the selected axes."""
        active = [idx for idx, ax_id in enumerate(self._axisId)
                  if self._menu.IsChecked(ax_id)]
        return active
