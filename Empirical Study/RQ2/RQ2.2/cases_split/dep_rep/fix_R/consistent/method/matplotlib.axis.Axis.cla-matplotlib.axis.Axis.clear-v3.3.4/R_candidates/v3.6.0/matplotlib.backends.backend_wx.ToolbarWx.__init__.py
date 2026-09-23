    def __init__(self, toolmanager, parent=None, style=wx.TB_BOTTOM):
        if parent is None:
            parent = toolmanager.canvas.GetParent()
        ToolContainerBase.__init__(self, toolmanager)
        wx.ToolBar.__init__(self, parent, -1, style=style)
        self._space = self.AddStretchableSpace()
        self._label_text = wx.StaticText(self, style=wx.ALIGN_RIGHT)
        self.AddControl(self._label_text)
        self._toolitems = {}
        self._groups = {}  # Mapping of groups to the separator after them.
