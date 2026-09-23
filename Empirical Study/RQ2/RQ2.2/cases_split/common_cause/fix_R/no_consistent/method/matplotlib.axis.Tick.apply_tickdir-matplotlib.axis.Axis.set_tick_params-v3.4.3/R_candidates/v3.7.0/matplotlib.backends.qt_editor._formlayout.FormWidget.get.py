    def get(self):
        valuelist = []
        for index, (label, value) in enumerate(self.data):
            field = self.widgets[index]
            if label is None:
                # Separator / Comment
                continue
            elif tuple_to_qfont(value) is not None:
                value = field.get_font()
            elif isinstance(value, str) or mcolors.is_color_like(value):
                value = str(field.text())
            elif isinstance(value, (list, tuple)):
                index = int(field.currentIndex())
                if isinstance(value[0], (list, tuple)):
                    value = value[index][0]
                else:
                    value = value[index]
            elif isinstance(value, bool):
                value = field.isChecked()
            elif isinstance(value, Integral):
                value = int(field.value())
            elif isinstance(value, Real):
                value = float(str(field.text()))
            elif isinstance(value, datetime.datetime):
                datetime_ = field.dateTime()
                if hasattr(datetime_, "toPyDateTime"):
                    value = datetime_.toPyDateTime()
                else:
                    value = datetime_.toPython()
            elif isinstance(value, datetime.date):
                date_ = field.date()
                if hasattr(date_, "toPyDate"):
                    value = date_.toPyDate()
                else:
                    value = date_.toPython()
            else:
                value = eval(str(field.text()))
            valuelist.append(value)
        return valuelist
