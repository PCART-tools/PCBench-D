    def __init__(self, parent):

        wx.Button.__init__(self, parent, _NTB_AXISMENU_BUTTON, "Axes:        ",
                           style=wx.BU_EXACTFIT)
        self._toolbar = parent
        self._menu = wx.Menu()
        self._axisId = []
        # First two menu items never change...
        self._allId = wx.NewId()
        self._invertId = wx.NewId()
        self._menu.Append(self._allId, "All", "Select all axes", False)
        self._menu.Append(self._invertId, "Invert", "Invert axes selected",
                          False)
        self._menu.AppendSeparator()

        self.Bind(wx.EVT_BUTTON, self._onMenuButton, id=_NTB_AXISMENU_BUTTON)
        self.Bind(wx.EVT_MENU, self._handleSelectAllAxes, id=self._allId)
        self.Bind(wx.EVT_MENU, self._handleInvertAxesSelected,
                  id=self._invertId)
