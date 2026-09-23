class BlockingContourLabeler(BlockingMouseInput):
    """
    Callable for retrieving mouse clicks and key presses in a blocking way.

    Used to place contour labels.
    """

    def __init__(self, cs):
        self.cs = cs
        super().__init__(fig=cs.axes.figure)

    def add_click(self, event):
        self.button1(event)

    def pop_click(self, event, index=-1):
        self.button3(event)

    def button1(self, event):
        """
        Process an button-1 event (add a label to a contour).

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        # Shorthand
        if event.inaxes == self.cs.ax:
            self.cs.add_label_near(event.x, event.y, self.inline,
                                   inline_spacing=self.inline_spacing,
                                   transform=False)
            self.fig.canvas.draw()
        else:  # Remove event if not valid
            BlockingInput.pop(self)

    def button3(self, event):
        """
        Process an button-3 event (remove a label if not in inline mode).

        Unfortunately, if one is doing inline labels, then there is currently
        no way to fix the broken contour - once humpty-dumpty is broken, he
        can't be put back together.  In inline mode, this does nothing.

        Parameters
        ----------
        event : `~.backend_bases.MouseEvent`
        """
        if self.inline:
            pass
        else:
            self.cs.pop_label()
            self.cs.ax.figure.canvas.draw()

    def __call__(self, inline, inline_spacing=5, n=-1, timeout=-1):
        self.inline = inline
        self.inline_spacing = inline_spacing
        super().__call__(n=n, timeout=timeout, show_clicks=False)
