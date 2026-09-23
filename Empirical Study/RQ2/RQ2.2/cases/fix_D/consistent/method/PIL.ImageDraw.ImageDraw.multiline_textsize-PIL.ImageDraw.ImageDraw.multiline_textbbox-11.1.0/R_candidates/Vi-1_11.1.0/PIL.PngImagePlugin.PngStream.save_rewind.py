    def save_rewind(self) -> None:
        self.rewind_state = _RewindState(
            self.im_info.copy(),
            self.im_tile,
            self._seq_num,
        )
