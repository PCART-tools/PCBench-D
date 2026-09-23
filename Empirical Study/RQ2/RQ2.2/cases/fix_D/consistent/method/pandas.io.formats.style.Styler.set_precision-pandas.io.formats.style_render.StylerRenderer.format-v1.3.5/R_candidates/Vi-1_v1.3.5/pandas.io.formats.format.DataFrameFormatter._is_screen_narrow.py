    def _is_screen_narrow(self, max_width) -> bool:
        return bool(self.max_cols == 0 and len(self.frame.columns) > max_width)
