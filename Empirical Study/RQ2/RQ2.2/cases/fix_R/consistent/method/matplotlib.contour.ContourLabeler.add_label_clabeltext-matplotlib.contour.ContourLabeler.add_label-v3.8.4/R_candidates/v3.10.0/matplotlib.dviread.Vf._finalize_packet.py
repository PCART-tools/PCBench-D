    def _finalize_packet(self, packet_char, packet_width):
        if not self._missing_font:  # Otherwise we don't have full glyph definition.
            self._chars[packet_char] = Page(
                text=self.text, boxes=self.boxes, width=packet_width,
                height=None, descent=None)
        self.state = _dvistate.outer
