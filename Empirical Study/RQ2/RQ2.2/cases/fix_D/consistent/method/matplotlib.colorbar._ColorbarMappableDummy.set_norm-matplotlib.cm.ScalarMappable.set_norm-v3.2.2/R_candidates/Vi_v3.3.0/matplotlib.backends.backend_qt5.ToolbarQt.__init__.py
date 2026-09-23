    def __init__(self, toolmanager, parent):
        ToolContainerBase.__init__(self, toolmanager)
        QtWidgets.QToolBar.__init__(self, parent)
        self.setAllowedAreas(
            QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
        message_label = QtWidgets.QLabel("")
        message_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        message_label.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Ignored))
        self._message_action = self.addWidget(message_label)
        self._toolitems = {}
        self._groups = {}
