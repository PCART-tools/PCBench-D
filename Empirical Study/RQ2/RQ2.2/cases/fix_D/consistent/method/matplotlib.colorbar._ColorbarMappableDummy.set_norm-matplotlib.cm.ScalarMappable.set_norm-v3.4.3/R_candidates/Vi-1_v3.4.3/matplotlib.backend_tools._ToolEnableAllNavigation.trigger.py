    def trigger(self, sender, event, data=None):
        mpl.backend_bases.key_press_handler(event, self.figure.canvas, None)
