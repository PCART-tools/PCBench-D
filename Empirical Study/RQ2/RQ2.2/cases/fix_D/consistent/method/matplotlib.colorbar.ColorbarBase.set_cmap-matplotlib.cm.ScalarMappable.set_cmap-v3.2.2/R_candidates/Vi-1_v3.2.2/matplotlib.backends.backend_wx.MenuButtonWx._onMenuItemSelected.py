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
