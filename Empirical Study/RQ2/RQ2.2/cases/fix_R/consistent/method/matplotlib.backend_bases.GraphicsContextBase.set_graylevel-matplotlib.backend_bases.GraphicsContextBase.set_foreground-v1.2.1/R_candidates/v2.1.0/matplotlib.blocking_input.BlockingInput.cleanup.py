    def cleanup(self):
        """Disconnect all callbacks"""
        for cb in self.callbacks:
            self.fig.canvas.mpl_disconnect(cb)

        self.callbacks = []
