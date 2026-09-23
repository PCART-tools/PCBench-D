    def _get_tool_pos(self, tool):
        """
        Find the position (index) of a wx.ToolBarToolBase in a ToolBar.

        ``ToolBar.GetToolPos`` is not useful because wx assigns the same Id to
        all Separators and StretchableSpaces.
        """
        pos, = [pos for pos in range(self.ToolsCount)
                if self.GetToolByPos(pos) == tool]
        return pos
