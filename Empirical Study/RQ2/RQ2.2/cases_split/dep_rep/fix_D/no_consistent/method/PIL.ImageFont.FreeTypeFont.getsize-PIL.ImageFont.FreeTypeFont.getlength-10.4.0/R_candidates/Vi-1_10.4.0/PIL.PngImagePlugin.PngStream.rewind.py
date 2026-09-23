    def rewind(self) -> None:
        self.im_info = self.rewind_state["info"].copy()
        self.im_tile = self.rewind_state["tile"]
        self._seq_num = self.rewind_state["seq_num"]
