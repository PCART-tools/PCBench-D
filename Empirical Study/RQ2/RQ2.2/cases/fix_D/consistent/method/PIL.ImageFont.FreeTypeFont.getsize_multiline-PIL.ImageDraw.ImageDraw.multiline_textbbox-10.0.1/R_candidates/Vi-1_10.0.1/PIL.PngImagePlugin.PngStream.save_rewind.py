    def save_rewind(self):
        self.rewind_state = {
            "info": self.im_info.copy(),
            "tile": self.im_tile,
            "seq_num": self._seq_num,
        }
