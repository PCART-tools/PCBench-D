    def set_val(self, val):
        newval = str(val)
        if self.text == newval:
            return
        self.text = newval
        self.text_disp.remove()
        self.text_disp = self._make_text_disp(self.text)
        self._rendercursor()
        self._notify_change_observers()
        self._notify_submit_observers()
