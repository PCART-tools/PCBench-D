    def trigger(self, sender, event, data):
        """Call `draw_rubberband` or `remove_rubberband` based on data"""
        if not self.figure.canvas.widgetlock.available(sender):
            return
        if data is not None:
            self.draw_rubberband(*data)
        else:
            self.remove_rubberband()
