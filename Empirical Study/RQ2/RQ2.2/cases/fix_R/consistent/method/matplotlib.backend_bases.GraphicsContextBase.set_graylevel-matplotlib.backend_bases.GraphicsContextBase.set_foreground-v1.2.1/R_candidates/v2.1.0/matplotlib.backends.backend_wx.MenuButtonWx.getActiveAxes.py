    def getActiveAxes(self):
        """Return a list of the selected axes."""
        active = []
        for i in range(len(self._axisId)):
            if self._menu.IsChecked(self._axisId[i]):
                active.append(i)
        return active
