    def __init__(self, toolmanager, parent, style=wx.TB_HORIZONTAL):
        ToolContainerBase.__init__(self, toolmanager)
        wx.ToolBar.__init__(self, parent, -1, style=style)
        self._toolitems = {}
        self._groups = {}
        self._last = None
