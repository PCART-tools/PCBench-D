    def rewind(self):
        self.im_info = self.rewind_state["info"]
        self.im_tile = self.rewind_state["tile"]
        self._seq_num = self.rewind_state["seq_num"]
