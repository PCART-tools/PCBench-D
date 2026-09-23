    def destroy(self, *args, **kwargs):
        if self.window is not None:
            self.window.destroy()
            self.window = None
