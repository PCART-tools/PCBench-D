    def __init__(self, toolmanager, parent, style=wx.TB_HORIZONTAL):
        ToolContainerBase.__init__(self, toolmanager)
        wx.ToolBar.__init__(self, parent, -1, style=style)
        self._space = self.AddStretchableSpace()
        self._label_text = wx.StaticText(self)
        self.AddControl(self._label_text)
        self._toolitems = {}
        self._groups = {}  # Mapping of groups to the separator after them.
