    def _onMenuButton(self, evt):
        """Handle menu button pressed."""
        if wxc.is_phoenix:
            x, y = self.GetPosition()
            w, h = self.GetSize()
        else:
            x, y = self.GetPositionTuple()
            w, h = self.GetSizeTuple()
        self.PopupMenuXY(self._menu, x, y + h - 4)
        # When menu returned, indicate selection in button
        evt.Skip()
