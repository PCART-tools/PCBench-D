    @keyAutoRepeat.setter
    @cbook.deprecated("3.0", "Manually check `event.guiEvent.isAutoRepeat()` "
                      "in the event handler.")
    def keyAutoRepeat(self, val):
        self._keyautorepeat = bool(val)
