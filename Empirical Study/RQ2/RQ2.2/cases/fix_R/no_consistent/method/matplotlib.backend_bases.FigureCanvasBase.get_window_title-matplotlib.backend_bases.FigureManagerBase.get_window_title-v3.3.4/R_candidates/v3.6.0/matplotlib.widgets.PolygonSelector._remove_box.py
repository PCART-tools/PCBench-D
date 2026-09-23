    def _remove_box(self):
        if self._box is not None:
            self._box.set_visible(False)
            self._box = None
