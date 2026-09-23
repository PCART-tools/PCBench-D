    def __init__(self, targetfig, parent):
        super().__init__()
        self.setObjectName("SubplotTool")
        self._spinboxes = {}
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)
        for group, spinboxes, buttons in [
                ("Borders",
                 ["top", "bottom", "left", "right"],
                 [("Export values", self._export_values)]),
                ("Spacings",
                 ["hspace", "wspace"],
                 [("Tight layout", self._tight_layout),
                  ("Reset", self._reset),
                  ("Close", self.close)])]:
            layout = QtWidgets.QVBoxLayout()
            main_layout.addLayout(layout)
            box = QtWidgets.QGroupBox(group)
            layout.addWidget(box)
            inner = QtWidgets.QFormLayout(box)
            for name in spinboxes:
                self._spinboxes[name] = spinbox = QtWidgets.QDoubleSpinBox()
                spinbox.setValue(getattr(targetfig.subplotpars, name))
                spinbox.setRange(0, 1)
                spinbox.setDecimals(3)
                spinbox.setSingleStep(0.005)
                spinbox.setKeyboardTracking(False)
                spinbox.valueChanged.connect(self._on_value_changed)
                inner.addRow(name, spinbox)
            layout.addStretch(1)
            for name, method in buttons:
                button = QtWidgets.QPushButton(name)
                # Don't trigger on <enter>, which is used to input values.
                button.setAutoDefault(False)
                button.clicked.connect(method)
                layout.addWidget(button)
                if name == "Close":
                    button.setFocus()
        self._figure = targetfig
        self._defaults = {spinbox: vars(self._figure.subplotpars)[attr]
                          for attr, spinbox in self._spinboxes.items()}
        self._export_values_dialog = None
