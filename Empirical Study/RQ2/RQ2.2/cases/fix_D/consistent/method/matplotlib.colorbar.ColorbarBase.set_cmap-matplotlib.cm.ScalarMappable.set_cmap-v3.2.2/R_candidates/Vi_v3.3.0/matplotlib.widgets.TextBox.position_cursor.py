    def position_cursor(self, x):
        # now, we have to figure out where the cursor goes.
        # approximate it based on assuming all characters the same length
        if len(self.text) == 0:
            self.cursor_index = 0
        else:
            bb = self.text_disp.get_window_extent()
            ratio = np.clip((x - bb.x0) / bb.width, 0, 1)
            self.cursor_index = int(len(self.text) * ratio)
        self._rendercursor()
