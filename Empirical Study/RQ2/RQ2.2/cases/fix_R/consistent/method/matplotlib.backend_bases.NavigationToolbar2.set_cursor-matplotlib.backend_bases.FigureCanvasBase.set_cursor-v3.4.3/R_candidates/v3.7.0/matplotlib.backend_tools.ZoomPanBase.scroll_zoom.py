    def scroll_zoom(self, event):
        # https://gist.github.com/tacaswell/3144287
        if event.inaxes is None:
            return

        if event.button == 'up':
            # deal with zoom in
            scl = self.base_scale
        elif event.button == 'down':
            # deal with zoom out
            scl = 1/self.base_scale
        else:
            # deal with something that should never happen
            scl = 1

        ax = event.inaxes
        ax._set_view_from_bbox([event.x, event.y, scl])

        # If last scroll was done within the timing threshold, delete the
        # previous view
        if (time.time()-self.lastscroll) < self.scrollthresh:
            self.toolmanager.get_tool(_views_positions).back()

        self.figure.canvas.draw_idle()  # force re-draw

        self.lastscroll = time.time()
        self.toolmanager.get_tool(_views_positions).push_current()
