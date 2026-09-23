    def _onMenuButton(self, evt):
        """Handle menu button pressed."""
        x, y = self.GetPosition()
        w, h = self.GetSize()
        self.PopupMenuXY(self._menu, x, y + h - 4)
        # When menu returned, indicate selection in button
        evt.Skip()
