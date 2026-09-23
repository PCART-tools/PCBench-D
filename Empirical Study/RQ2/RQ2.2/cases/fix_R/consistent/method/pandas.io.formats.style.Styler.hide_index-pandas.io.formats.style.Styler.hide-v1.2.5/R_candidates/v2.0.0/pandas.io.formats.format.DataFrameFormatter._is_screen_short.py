    def _is_screen_short(self, max_height) -> bool:
        return bool(self.max_rows == 0 and len(self.frame) > max_height)
