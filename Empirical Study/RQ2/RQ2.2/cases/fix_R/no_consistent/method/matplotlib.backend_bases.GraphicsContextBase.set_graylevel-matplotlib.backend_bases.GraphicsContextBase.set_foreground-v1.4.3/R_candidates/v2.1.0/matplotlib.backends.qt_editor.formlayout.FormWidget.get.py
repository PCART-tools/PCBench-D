    def get(self):
        valuelist = []
        for index, (label, value) in enumerate(self.data):
            field = self.widgets[index]
            if label is None:
                # Separator / Comment
                continue
            elif tuple_to_qfont(value) is not None:
                value = field.get_font()
            elif (isinstance(value, six.string_types)
                  or mcolors.is_color_like(value)):
                value = six.text_type(field.text())
            elif isinstance(value, (list, tuple)):
                index = int(field.currentIndex())
                if isinstance(value[0], (list, tuple)):
                    value = value[index][0]
                else:
                    value = value[index]
            elif isinstance(value, bool):
                value = field.checkState() == QtCore.Qt.Checked
            elif isinstance(value, float):
                value = float(str(field.text()))
            elif isinstance(value, int):
                value = int(field.value())
            elif isinstance(value, datetime.datetime):
                value = field.dateTime().toPyDateTime()
            elif isinstance(value, datetime.date):
                value = field.date().toPyDate()
            else:
                value = eval(str(field.text()))
            valuelist.append(value)
        return valuelist
