    def cleanup(self, event=None):
        # clean the figure
        if self.show_clicks:

            for mark in self.marks:
                mark.remove()
            self.marks = []

            self.fig.canvas.draw()

        # Call base class to remove callbacks
        BlockingInput.cleanup(self)
