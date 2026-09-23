    def position_cursor(self, x):
        # now, we have to figure out where the cursor goes.
        # approximate it based on assuming all characters the same length
        if len(self.text) == 0:
            self.cursor_index = 0
        else:
            bb = self.text_disp.get_window_extent()

            trans = self.ax.transData
            inv = self.ax.transData.inverted()
            bb = trans.transform(inv.transform(bb))

            text_start = bb[0, 0]
            text_end = bb[1, 0]

            ratio = (x - text_start) / (text_end - text_start)

            if ratio < 0:
                ratio = 0
            if ratio > 1:
                ratio = 1

            self.cursor_index = int(len(self.text) * ratio)

        self._rendercursor()
