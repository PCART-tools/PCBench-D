    def _init_toolbar(self):
        DEBUG_MSG("_init_toolbar", 1, self)

        self._parent = self.canvas.GetParent()

        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = (
                self.AddTool(
                    -1,
                    bitmap=_load_bitmap(image_file + ".png"),
                    bmpDisabled=wx.NullBitmap,
                    label=text, shortHelp=text, longHelp=tooltip_text,
                    kind=(wx.ITEM_CHECK if text in ["Pan", "Zoom"]
                          else wx.ITEM_NORMAL))
                .Id)
            self.Bind(wx.EVT_TOOL, getattr(self, callback),
                      id=self.wx_ids[text])

        self.Realize()
