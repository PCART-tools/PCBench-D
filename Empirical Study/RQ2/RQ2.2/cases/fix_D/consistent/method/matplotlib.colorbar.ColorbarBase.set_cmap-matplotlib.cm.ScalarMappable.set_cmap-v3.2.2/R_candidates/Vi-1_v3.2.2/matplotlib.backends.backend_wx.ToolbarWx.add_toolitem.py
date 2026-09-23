    def add_toolitem(
        self, name, group, position, image_file, description, toggle):

        before, group = self._add_to_group(group, name, position)
        idx = self.GetToolPos(before.Id)
        if image_file:
            bmp = _load_bitmap(image_file)
            kind = wx.ITEM_NORMAL if not toggle else wx.ITEM_CHECK
            tool = self.InsertTool(idx, -1, name, bmp, wx.NullBitmap, kind,
                                   description or "")
        else:
            size = (self.GetTextExtent(name)[0]+10, -1)
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
        group.insert(position, tool)
        self._toolitems[name].append((tool, handler))
