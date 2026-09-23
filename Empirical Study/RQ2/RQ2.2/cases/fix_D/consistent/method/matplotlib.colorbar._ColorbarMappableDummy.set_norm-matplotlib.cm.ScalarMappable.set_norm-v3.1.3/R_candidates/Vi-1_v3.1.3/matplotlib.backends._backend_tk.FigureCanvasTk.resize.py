    def resize(self, event):
        width, height = event.width, event.height
        if self._resize_callback is not None:
            self._resize_callback(event)

        # compute desired figure size in inches
        dpival = self.figure.dpi
        winch = width / dpival
        hinch = height / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)

        self._tkcanvas.delete(self._tkphoto)
        self._tkphoto = tk.PhotoImage(
            master=self._tkcanvas, width=int(width), height=int(height))
        self._tkcanvas.create_image(
            int(width / 2), int(height / 2), image=self._tkphoto)
        self.resize_event()
        self.draw()

        # a resizing will in general move the pointer position
        # relative to the canvas, so process it as a motion notify
        # event.  An intended side effect of this call is to allow
        # window raises (which trigger a resize) to get the cursor
        # position to the mpl event framework so key presses which are
        # over the axes will work w/o clicks or explicit motion
        self._update_pointer_position(event)
