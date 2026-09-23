    def _rendercursor(self):
        # this is a hack to figure out where the cursor should go.
        # we draw the text up to where the cursor should go, measure
        # and save its dimensions, draw the real text, then put the cursor
        # at the saved dimensions

        # This causes a single extra draw if the figure has never been rendered
        # yet, which should be fine as we're going to repeatedly re-render the
        # figure later anyways.
        if self.ax.figure._cachedRenderer is None:
            self.ax.figure.canvas.draw()

        text = self.text_disp.get_text()  # Save value before overwriting it.
        widthtext = text[:self.cursor_index]
        self.text_disp.set_text(widthtext or ",")
        bb = self.text_disp.get_window_extent()
        if not widthtext:  # Use the comma for the height, but keep width to 0.
            bb.x1 = bb.x0
        self.cursor.set(
            segments=[[(bb.x1, bb.y0), (bb.x1, bb.y1)]], visible=True)
        self.text_disp.set_text(text)

        self.ax.figure.canvas.draw()
