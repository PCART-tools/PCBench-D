    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        if self.figure is None:
            return
        LocationEvent("figure_leave_event", self,
                      *self.mouseEventCoords(),
                      modifiers=self._mpl_modifiers(),
                      guiEvent=event)._process()
