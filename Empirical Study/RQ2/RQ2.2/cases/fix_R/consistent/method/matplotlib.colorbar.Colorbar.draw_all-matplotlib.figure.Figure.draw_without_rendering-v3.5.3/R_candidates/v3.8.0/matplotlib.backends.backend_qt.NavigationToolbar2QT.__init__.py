    def __init__(self, canvas, parent=None, coordinates=True):
        """coordinates: should we show the coordinates on the right?"""
        QtWidgets.QToolBar.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.ToolBarArea(
            _to_int(QtCore.Qt.ToolBarArea.TopToolBarArea) |
            _to_int(QtCore.Qt.ToolBarArea.BottomToolBarArea)))
        self.coordinates = coordinates
        self._actions = {}  # mapping of toolitem method names to QActions.
        self._subplot_dialog = None

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.addSeparator()
            else:
                a = self.addAction(self._icon(image_file + '.png'),
                                   text, getattr(self, callback))
                self._actions[callback] = a
                if callback in ['zoom', 'pan']:
                    a.setCheckable(True)
                if tooltip_text is not None:
                    a.setToolTip(tooltip_text)

        # Add the (x, y) location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        if self.coordinates:
            self.locLabel = QtWidgets.QLabel("", self)
            self.locLabel.setAlignment(QtCore.Qt.AlignmentFlag(
                _to_int(QtCore.Qt.AlignmentFlag.AlignRight) |
                _to_int(QtCore.Qt.AlignmentFlag.AlignVCenter)))

            self.locLabel.setSizePolicy(QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Ignored,
            ))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(True)

        NavigationToolbar2.__init__(self, canvas)
