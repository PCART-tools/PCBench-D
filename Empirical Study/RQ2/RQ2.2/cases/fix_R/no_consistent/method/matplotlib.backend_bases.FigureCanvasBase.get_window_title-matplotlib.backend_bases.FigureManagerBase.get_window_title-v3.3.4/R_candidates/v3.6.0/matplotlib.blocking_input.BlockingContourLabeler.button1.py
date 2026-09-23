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
