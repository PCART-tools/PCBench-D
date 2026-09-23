    def __init__(self, toolmanager, parent=None):
        ToolContainerBase.__init__(self, toolmanager)
        QtWidgets.QToolBar.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.ToolBarArea(
            _to_int(_enum("QtCore.Qt.ToolBarArea").TopToolBarArea) |
            _to_int(_enum("QtCore.Qt.ToolBarArea").BottomToolBarArea)))
        message_label = QtWidgets.QLabel("")
        message_label.setAlignment(QtCore.Qt.AlignmentFlag(
            _to_int(_enum("QtCore.Qt.AlignmentFlag").AlignRight) |
            _to_int(_enum("QtCore.Qt.AlignmentFlag").AlignVCenter)))
        message_label.setSizePolicy(QtWidgets.QSizePolicy(
            _enum("QtWidgets.QSizePolicy.Policy").Expanding,
            _enum("QtWidgets.QSizePolicy.Policy").Ignored,
        ))
        self._message_action = self.addWidget(message_label)
        self._toolitems = {}
        self._groups = {}
