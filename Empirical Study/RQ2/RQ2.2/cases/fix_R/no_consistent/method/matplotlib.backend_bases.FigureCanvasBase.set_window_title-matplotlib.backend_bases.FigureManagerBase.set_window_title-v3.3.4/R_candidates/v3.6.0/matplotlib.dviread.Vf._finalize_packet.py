    def _finalize_packet(self, packet_char, packet_width):
        self._chars[packet_char] = Page(
            text=self.text, boxes=self.boxes, width=packet_width,
            height=None, descent=None)
        self.state = _dvistate.outer
