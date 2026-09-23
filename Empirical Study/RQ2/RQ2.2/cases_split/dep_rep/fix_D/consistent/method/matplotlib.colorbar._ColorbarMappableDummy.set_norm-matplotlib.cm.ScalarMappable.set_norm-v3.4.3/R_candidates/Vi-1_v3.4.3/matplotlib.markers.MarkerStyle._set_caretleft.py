    def _set_caretleft(self):
        self._set_caretdown()
        self._transform = self._transform.rotate_deg(270)
