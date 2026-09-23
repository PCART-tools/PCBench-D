    def _init_toolbar(self):
        DEBUG_MSG("_init_toolbar", 1, self)

        self._parent = self.canvas.GetParent()

        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = wx.NewId()
            wxc._AddTool(self, self.wx_ids, text,
                        _load_bitmap(image_file + '.png'),
                        tooltip_text)

            self.Bind(wx.EVT_TOOL, getattr(self, callback),
                      id=self.wx_ids[text])

        self.Realize()
