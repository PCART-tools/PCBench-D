    def save_figure(self, *args):
        """Save the current figure."""
        self.canvas.send_event('save')
        return self.UNKNOWN_SAVED_STATUS
