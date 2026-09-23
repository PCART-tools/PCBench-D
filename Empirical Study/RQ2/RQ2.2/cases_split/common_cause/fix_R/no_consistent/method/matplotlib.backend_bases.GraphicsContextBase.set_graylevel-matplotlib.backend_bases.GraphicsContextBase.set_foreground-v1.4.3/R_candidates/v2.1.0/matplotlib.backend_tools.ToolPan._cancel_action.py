    def _cancel_action(self):
        self._button_pressed = None
        self._xypress = []
        self.figure.canvas.mpl_disconnect(self._idDrag)
        self.toolmanager.messagelock.release(self)
        self.toolmanager.get_tool(_views_positions).refresh_locators()
