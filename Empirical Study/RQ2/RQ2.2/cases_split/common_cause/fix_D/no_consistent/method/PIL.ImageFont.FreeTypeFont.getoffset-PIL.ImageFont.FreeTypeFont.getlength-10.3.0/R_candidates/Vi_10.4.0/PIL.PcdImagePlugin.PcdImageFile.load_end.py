    def load_end(self) -> None:
        if self.tile_post_rotate:
            # Handle rotated PCDs
            assert self.im is not None

            self.im = self.im.rotate(self.tile_post_rotate)
            self._size = self.im.size
