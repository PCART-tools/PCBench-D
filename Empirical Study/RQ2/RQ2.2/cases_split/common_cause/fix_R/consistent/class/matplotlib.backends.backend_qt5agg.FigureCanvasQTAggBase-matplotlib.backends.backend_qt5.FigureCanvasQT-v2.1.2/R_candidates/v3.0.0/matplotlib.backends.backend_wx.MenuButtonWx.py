class MenuButtonWx(wx.Button):
    """
    wxPython does not permit a menu to be incorporated directly into a toolbar.
    This class simulates the effect by associating a pop-up menu with a button
    in the toolbar, and managing this as though it were a menu.
    """

    def __init__(self, parent):

        wx.Button.__init__(self, parent, _NTB_AXISMENU_BUTTON, "Axes:        ",
                           style=wx.BU_EXACTFIT)
        self._toolbar = parent
        self._menu = wx.Menu()
        self._axisId = []
        # First two menu items never change...
        self._allId = wx.NewId()
        self._invertId = wx.NewId()
        self._menu.Append(self._allId, "All", "Select all axes", False)
        self._menu.Append(self._invertId, "Invert", "Invert axes selected",
                          False)
        self._menu.AppendSeparator()

        self.Bind(wx.EVT_BUTTON, self._onMenuButton, id=_NTB_AXISMENU_BUTTON)
        self.Bind(wx.EVT_MENU, self._handleSelectAllAxes, id=self._allId)
        self.Bind(wx.EVT_MENU, self._handleInvertAxesSelected,
                  id=self._invertId)

    def Destroy(self):
        self._menu.Destroy()
        self.Destroy()

    def _onMenuButton(self, evt):
        """Handle menu button pressed."""
        x, y = self.GetPosition()
        w, h = self.GetSize()
        self.PopupMenuXY(self._menu, x, y + h - 4)
        # When menu returned, indicate selection in button
        evt.Skip()

    def _handleSelectAllAxes(self, evt):
        """Called when the 'select all axes' menu item is selected."""
        if len(self._axisId) == 0:
            return
        for i in range(len(self._axisId)):
            self._menu.Check(self._axisId[i], True)
        self._toolbar.set_active(self.getActiveAxes())
        evt.Skip()

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

    def _onMenuItemSelected(self, evt):
        """Called whenever one of the specific axis menu items is selected"""
        current = self._menu.IsChecked(evt.GetId())
        if current:
            new = False
        else:
            new = True
        self._menu.Check(evt.GetId(), new)
        # Lines above would be deleted based on svn tracker ID 2841525;
        # not clear whether this matters or not.
        self._toolbar.set_active(self.getActiveAxes())
        evt.Skip()

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
        self._toolbar.set_active(list(range(maxAxis)))

    def getActiveAxes(self):
        """Return a list of the selected axes."""
        active = []
        for i in range(len(self._axisId)):
            if self._menu.IsChecked(self._axisId[i]):
                active.append(i)
        return active

    def updateButtonText(self, lst):
        """Update the list of selected axes in the menu button."""
        self.SetLabel(
            'Axes: ' + ','.join('%d' % (e + 1) for e in lst))
