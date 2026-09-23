    def _handleSelectAllAxes(self, evt):
        """Called when the 'select all axes' menu item is selected."""
        if len(self._axisId) == 0:
            return
        for i in range(len(self._axisId)):
            self._menu.Check(self._axisId[i], True)
        self._toolbar.set_active(self.getActiveAxes())
        evt.Skip()
