    def add_click(self, event):
        """Add the coordinates of an event to the list of clicks."""
        self.clicks.append((event.xdata, event.ydata))
        _log.info("input %i: %f, %f",
                  len(self.clicks), event.xdata, event.ydata)
        # If desired, plot up click.
        if self.show_clicks:
            line = mlines.Line2D([event.xdata], [event.ydata],
                                 marker='+', color='r')
            event.inaxes.add_line(line)
            self.marks.append(line)
            self.fig.canvas.draw()
