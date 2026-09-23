    def setup(self):
        for label, value in self.data:
            if DEBUG:
                print("value:", value)
            if label is None and value is None:
                # Separator: (None, None)
                self.formlayout.addRow(QtWidgets.QLabel(" "), QtWidgets.QLabel(" "))
                self.widgets.append(None)
                continue
            elif label is None:
                # Comment
                self.formlayout.addRow(QtWidgets.QLabel(value))
                self.widgets.append(None)
                continue
            elif tuple_to_qfont(value) is not None:
                field = FontLayout(value, self)
            elif (label.lower() not in BLACKLIST
                  and mcolors.is_color_like(value)):
                field = ColorLayout(to_qcolor(value), self)
            elif isinstance(value, six.string_types):
                field = QtWidgets.QLineEdit(value, self)
            elif isinstance(value, (list, tuple)):
                if isinstance(value, tuple):
                    value = list(value)
                selindex = value.pop(0)
                field = QtWidgets.QComboBox(self)
                if isinstance(value[0], (list, tuple)):
                    keys = [key for key, _val in value]
                    value = [val for _key, val in value]
                else:
                    keys = value
                field.addItems(value)
                if selindex in value:
                    selindex = value.index(selindex)
                elif selindex in keys:
                    selindex = keys.index(selindex)
                elif not isinstance(selindex, int):
                    warnings.warn(
                        "index '%s' is invalid (label: %s, value: %s)" %
                        (selindex, label, value))
                    selindex = 0
                field.setCurrentIndex(selindex)
            elif isinstance(value, bool):
                field = QtWidgets.QCheckBox(self)
                if value:
                    field.setCheckState(QtCore.Qt.Checked)
                else:
                    field.setCheckState(QtCore.Qt.Unchecked)
            elif isinstance(value, float):
                field = QtWidgets.QLineEdit(repr(value), self)
                field.setCursorPosition(0)
                field.setValidator(QtGui.QDoubleValidator(field))
                field.validator().setLocale(QtCore.QLocale("C"))
                dialog = self.get_dialog()
                dialog.register_float_field(field)
                field.textChanged.connect(lambda text: dialog.update_buttons())
            elif isinstance(value, int):
                field = QtWidgets.QSpinBox(self)
                field.setRange(-1e9, 1e9)
                field.setValue(value)
            elif isinstance(value, datetime.datetime):
                field = QtWidgets.QDateTimeEdit(self)
                field.setDateTime(value)
            elif isinstance(value, datetime.date):
                field = QtWidgets.QDateEdit(self)
                field.setDate(value)
            else:
                field = QtWidgets.QLineEdit(repr(value), self)
            self.formlayout.addRow(label, field)
            self.widgets.append(field)
