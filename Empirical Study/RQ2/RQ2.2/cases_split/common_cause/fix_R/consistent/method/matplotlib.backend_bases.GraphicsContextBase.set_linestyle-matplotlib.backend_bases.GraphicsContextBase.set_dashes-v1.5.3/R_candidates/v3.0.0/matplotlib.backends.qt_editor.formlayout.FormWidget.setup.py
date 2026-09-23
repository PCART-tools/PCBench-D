    def setup(self):
        for label, value in self.data:
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
            elif isinstance(value, str):
                field = QtWidgets.QLineEdit(value, self)
            elif isinstance(value, (list, tuple)):
                if isinstance(value, tuple):
                    value = list(value)
                # Note: get() below checks the type of value[0] in self.data so
                # it is essential that value gets modified in-place.
                # This means that the code is actually broken in the case where
                # value is a tuple, but fortunately we always pass a list...
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
                elif not isinstance(selindex, Integral):
                    warnings.warn(
                        "index '%s' is invalid (label: %s, value: %s)" %
                        (selindex, label, value), stacklevel=2)
                    selindex = 0
                field.setCurrentIndex(selindex)
            elif isinstance(value, bool):
                field = QtWidgets.QCheckBox(self)
                if value:
                    field.setCheckState(QtCore.Qt.Checked)
                else:
                    field.setCheckState(QtCore.Qt.Unchecked)
            elif isinstance(value, Integral):
                field = QtWidgets.QSpinBox(self)
                field.setRange(-1e9, 1e9)
                field.setValue(value)
            elif isinstance(value, Real):
                field = QtWidgets.QLineEdit(repr(value), self)
                field.setCursorPosition(0)
                field.setValidator(QtGui.QDoubleValidator(field))
                field.validator().setLocale(QtCore.QLocale("C"))
                dialog = self.get_dialog()
                dialog.register_float_field(field)
                field.textChanged.connect(lambda text: dialog.update_buttons())
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
