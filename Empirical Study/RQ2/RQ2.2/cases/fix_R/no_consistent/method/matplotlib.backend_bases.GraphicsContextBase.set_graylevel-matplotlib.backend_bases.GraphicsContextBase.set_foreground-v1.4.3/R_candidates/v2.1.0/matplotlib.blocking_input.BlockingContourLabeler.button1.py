    def button1(self, event):
        """
        This will be called if an event involving a button other than
        2 or 3 occcurs.  This will add a label to a contour.
        """

        # Shorthand
        if event.inaxes == self.cs.ax:
            self.cs.add_label_near(event.x, event.y, self.inline,
                                   inline_spacing=self.inline_spacing,
                                   transform=False)
            self.fig.canvas.draw()
        else:  # Remove event if not valid
            BlockingInput.pop(self)
