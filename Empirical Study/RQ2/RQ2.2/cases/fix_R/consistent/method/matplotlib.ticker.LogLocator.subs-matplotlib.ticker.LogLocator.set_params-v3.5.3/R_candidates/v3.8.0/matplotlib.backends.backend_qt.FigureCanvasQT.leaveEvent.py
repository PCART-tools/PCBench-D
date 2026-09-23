    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        LocationEvent("figure_leave_event", self,
                      *self.mouseEventCoords(),
                      modifiers=self._mpl_modifiers(),
                      guiEvent=event)._process()
