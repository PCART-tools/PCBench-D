    def _cancel_action(self):
        self._button_pressed = None
        self._xypress = []
        self.figure.canvas.mpl_disconnect(self._id_drag)
        self.toolmanager.messagelock.release(self)
        self.figure.canvas.draw_idle()
