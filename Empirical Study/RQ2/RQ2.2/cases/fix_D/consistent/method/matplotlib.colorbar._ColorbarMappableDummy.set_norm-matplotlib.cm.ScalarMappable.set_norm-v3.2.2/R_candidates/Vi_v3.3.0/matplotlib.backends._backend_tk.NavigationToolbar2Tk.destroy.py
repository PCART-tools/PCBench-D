    def destroy(self, *args):
        del self.message
        tk.Frame.destroy(self, *args)
