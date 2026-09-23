    def draw(self):
        """Draw the figure with Agg, and queue a request for a Qt draw.
        """
        # The Agg draw is done here; delaying causes problems with code that
        # uses the result of the draw() to update plot elements.
        super(FigureCanvasQTAggBase, self).draw()
        self.update()
