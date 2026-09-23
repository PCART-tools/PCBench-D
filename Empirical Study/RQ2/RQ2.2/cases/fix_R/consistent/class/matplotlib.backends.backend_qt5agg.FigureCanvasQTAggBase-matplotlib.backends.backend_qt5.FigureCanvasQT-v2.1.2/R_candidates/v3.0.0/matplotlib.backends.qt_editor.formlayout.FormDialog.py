class FormDialog(QtWidgets.QDialog):
    """Form Dialog"""
    def __init__(self, data, title="", comment="",
                 icon=None, parent=None, apply=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.apply_callback = apply

        # Form
        if isinstance(data[0][0], (list, tuple)):
            self.formwidget = FormTabWidget(data, comment=comment,
                                            parent=self)
        elif len(data[0]) == 3:
            self.formwidget = FormComboWidget(data, comment=comment,
                                              parent=self)
        else:
            self.formwidget = FormWidget(data, comment=comment,
                                         parent=self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.formwidget)

        self.float_fields = []
        self.formwidget.setup()

        # Button box
        self.bbox = bbox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.formwidget.update_buttons.connect(self.update_buttons)
        if self.apply_callback is not None:
            apply_btn = bbox.addButton(QtWidgets.QDialogButtonBox.Apply)
            apply_btn.clicked.connect(self.apply)

        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)

        self.setLayout(layout)

        self.setWindowTitle(title)
        if not isinstance(icon, QtGui.QIcon):
            icon = QtWidgets.QWidget().style().standardIcon(QtWidgets.QStyle.SP_MessageBoxQuestion)
        self.setWindowIcon(icon)

    def register_float_field(self, field):
        self.float_fields.append(field)

    def update_buttons(self):
        valid = True
        for field in self.float_fields:
            if not is_edit_valid(field):
                valid = False
        for btn_type in (QtWidgets.QDialogButtonBox.Ok,
                         QtWidgets.QDialogButtonBox.Apply):
            btn = self.bbox.button(btn_type)
            if btn is not None:
                btn.setEnabled(valid)

    def accept(self):
        self.data = self.formwidget.get()
        QtWidgets.QDialog.accept(self)

    def reject(self):
        self.data = None
        QtWidgets.QDialog.reject(self)

    def apply(self):
        self.apply_callback(self.formwidget.get())

    def get(self):
        """Return form result"""
        return self.data
