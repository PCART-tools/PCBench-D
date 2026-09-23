    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor(
            self._color, self.parentWidget(), "",
            _enum("QtWidgets.QColorDialog.ColorDialogOption").ShowAlphaChannel)
        if color.isValid():
            self.set_color(color)
