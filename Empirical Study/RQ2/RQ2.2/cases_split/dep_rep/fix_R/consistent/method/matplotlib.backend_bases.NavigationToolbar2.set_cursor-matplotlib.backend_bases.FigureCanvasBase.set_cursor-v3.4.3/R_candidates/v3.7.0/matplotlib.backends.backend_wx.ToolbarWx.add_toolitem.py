    def add_toolitem(self, name, group, position, image_file, description,
                     toggle):
        # Find or create the separator that follows this group.
        if group not in self._groups:
            self._groups[group] = self.InsertSeparator(
                self._get_tool_pos(self._space))
        sep = self._groups[group]
        # List all separators.
        seps = [t for t in map(self.GetToolByPos, range(self.ToolsCount))
                if t.IsSeparator() and not t.IsStretchableSpace()]
        # Find where to insert the tool.
        if position >= 0:
            # Find the start of the group by looking for the separator
            # preceding this one; then move forward from it.
            start = (0 if sep == seps[0]
                     else self._get_tool_pos(seps[seps.index(sep) - 1]) + 1)
        else:
            # Move backwards from this separator.
            start = self._get_tool_pos(sep) + 1
        idx = start + position
        if image_file:
            bmp = NavigationToolbar2Wx._icon(image_file)
            kind = wx.ITEM_NORMAL if not toggle else wx.ITEM_CHECK
            tool = self.InsertTool(idx, -1, name, bmp, wx.NullBitmap, kind,
                                   description or "")
        else:
            size = (self.GetTextExtent(name)[0] + 10, -1)
            if toggle:
                control = wx.ToggleButton(self, -1, name, size=size)
            else:
                control = wx.Button(self, -1, name, size=size)
            tool = self.InsertControl(idx, control, label=name)
        self.Realize()

        def handler(event):
            self.trigger_tool(name)

        if image_file:
            self.Bind(wx.EVT_TOOL, handler, tool)
        else:
            control.Bind(wx.EVT_LEFT_DOWN, handler)

        self._toolitems.setdefault(name, [])
        self._toolitems[name].append((tool, handler))
