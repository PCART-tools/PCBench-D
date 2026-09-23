    def enterEvent(self, event):
        # Force querying of the modifiers, as the cached modifier state can
        # have been invalidated while the window was out of focus.
        mods = QtWidgets.QApplication.instance().queryKeyboardModifiers()
        LocationEvent("figure_enter_event", self,
                      *self.mouseEventCoords(event),
                      modifiers=self._mpl_modifiers(mods),
                      guiEvent=event)._process()
