    def _set_caretup(self):
        self._set_caretdown()
        self._transform = self._transform.rotate_deg(180)
