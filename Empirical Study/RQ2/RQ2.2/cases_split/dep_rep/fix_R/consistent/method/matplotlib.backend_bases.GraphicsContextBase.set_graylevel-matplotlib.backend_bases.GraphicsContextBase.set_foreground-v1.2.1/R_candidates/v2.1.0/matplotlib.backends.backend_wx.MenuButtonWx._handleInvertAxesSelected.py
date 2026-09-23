    def _handleInvertAxesSelected(self, evt):
        """Called when the invert all menu item is selected"""
        if len(self._axisId) == 0:
            return
        for i in range(len(self._axisId)):
            if self._menu.IsChecked(self._axisId[i]):
                self._menu.Check(self._axisId[i], False)
            else:
                self._menu.Check(self._axisId[i], True)
        self._toolbar.set_active(self.getActiveAxes())
        evt.Skip()
