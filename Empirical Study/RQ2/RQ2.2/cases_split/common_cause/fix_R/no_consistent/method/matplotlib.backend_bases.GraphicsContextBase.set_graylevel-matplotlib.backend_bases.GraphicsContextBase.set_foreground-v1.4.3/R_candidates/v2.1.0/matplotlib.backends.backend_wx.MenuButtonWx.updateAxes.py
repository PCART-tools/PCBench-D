    def updateAxes(self, maxAxis):
        """Ensures that there are entries for max_axis axes in the menu
        (selected by default)."""
        if maxAxis > len(self._axisId):
            for i in range(len(self._axisId) + 1, maxAxis + 1, 1):
                menuId = wx.NewId()
                self._axisId.append(menuId)
                self._menu.Append(menuId, "Axis %d" % i,
                                  "Select axis %d" % i,
                                  True)
                self._menu.Check(menuId, True)
                self.Bind(wx.EVT_MENU, self._onMenuItemSelected, id=menuId)
        elif maxAxis < len(self._axisId):
            for menuId in self._axisId[maxAxis:]:
                self._menu.Delete(menuId)
            self._axisId = self._axisId[:maxAxis]
        self._toolbar.set_active(list(xrange(maxAxis)))
