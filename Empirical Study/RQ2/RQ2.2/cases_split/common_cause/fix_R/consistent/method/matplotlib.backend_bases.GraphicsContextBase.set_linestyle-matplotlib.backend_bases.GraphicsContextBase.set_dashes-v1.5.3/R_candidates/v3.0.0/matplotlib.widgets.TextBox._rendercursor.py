    def _rendercursor(self):
        # this is a hack to figure out where the cursor should go.
        # we draw the text up to where the cursor should go, measure
        # and save its dimensions, draw the real text, then put the cursor
        # at the saved dimensions

        widthtext = self.text[:self.cursor_index]
        no_text = False
        if(widthtext == "" or widthtext == " " or widthtext == "  "):
            no_text = widthtext == ""
            widthtext = ","

        wt_disp = self._make_text_disp(widthtext)

        self.ax.figure.canvas.draw()
        bb = wt_disp.get_window_extent()
        inv = self.ax.transData.inverted()
        bb = inv.transform(bb)
        wt_disp.set_visible(False)
        if no_text:
            bb[1, 0] = bb[0, 0]
        # hack done
        self.cursor.set_visible(False)

        self.cursor = self.ax.vlines(bb[1, 0], bb[0, 1], bb[1, 1])
        self.ax.figure.canvas.draw()
