    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        FigureCanvasBase.leave_notify_event(self, guiEvent=event)
