    def __init__(self, toolmanager, parent=None):
        ToolContainerBase.__init__(self, toolmanager)
        QtWidgets.QToolBar.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.ToolBarArea(
            _to_int(QtCore.Qt.ToolBarArea.TopToolBarArea) |
            _to_int(QtCore.Qt.ToolBarArea.BottomToolBarArea)))
        message_label = QtWidgets.QLabel("")
        message_label.setAlignment(QtCore.Qt.AlignmentFlag(
            _to_int(QtCore.Qt.AlignmentFlag.AlignRight) |
            _to_int(QtCore.Qt.AlignmentFlag.AlignVCenter)))
        message_label.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Ignored,
        ))
        self._message_action = self.addWidget(message_label)
        self._toolitems = {}
        self._groups = {}
