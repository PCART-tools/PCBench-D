    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor(
            self._color, self.parentWidget(), "",
            QtWidgets.QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.set_color(color)
