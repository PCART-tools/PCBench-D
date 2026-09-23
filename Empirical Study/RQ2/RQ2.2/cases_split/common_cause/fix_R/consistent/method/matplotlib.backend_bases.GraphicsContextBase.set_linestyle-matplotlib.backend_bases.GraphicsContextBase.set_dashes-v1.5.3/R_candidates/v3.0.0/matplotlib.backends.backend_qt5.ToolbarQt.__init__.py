    def __init__(self, toolmanager, parent):
        ToolContainerBase.__init__(self, toolmanager)
        QtWidgets.QToolBar.__init__(self, parent)
        self._toolitems = {}
        self._groups = {}
