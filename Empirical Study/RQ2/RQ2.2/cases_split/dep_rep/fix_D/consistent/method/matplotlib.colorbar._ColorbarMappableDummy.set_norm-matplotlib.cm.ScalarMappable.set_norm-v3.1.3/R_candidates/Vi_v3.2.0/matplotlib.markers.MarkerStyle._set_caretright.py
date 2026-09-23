    def _set_caretright(self):
        self._set_caretdown()
        self._transform = self._transform.rotate_deg(90)
