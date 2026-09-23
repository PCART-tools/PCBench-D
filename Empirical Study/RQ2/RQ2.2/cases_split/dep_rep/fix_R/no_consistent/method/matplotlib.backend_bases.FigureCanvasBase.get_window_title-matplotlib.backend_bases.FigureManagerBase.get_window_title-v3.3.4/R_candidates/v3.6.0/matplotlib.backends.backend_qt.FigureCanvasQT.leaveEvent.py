    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        LocationEvent("figure_leave_event", self,
                      *self.mouseEventCoords(),
                      guiEvent=event)._process()
