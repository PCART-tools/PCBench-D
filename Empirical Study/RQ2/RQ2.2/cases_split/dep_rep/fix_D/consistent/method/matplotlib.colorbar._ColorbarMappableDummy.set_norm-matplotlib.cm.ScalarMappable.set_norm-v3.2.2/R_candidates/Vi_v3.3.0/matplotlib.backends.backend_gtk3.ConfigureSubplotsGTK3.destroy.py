    @cbook.deprecated("3.2")
    def destroy(self, *args):
        self.window.destroy()
        self.window = None
