    def read_boxes(self):
        size = self.remaining_in_box
        data = self._read_bytes(size)
        return BoxReader(io.BytesIO(data), size)
