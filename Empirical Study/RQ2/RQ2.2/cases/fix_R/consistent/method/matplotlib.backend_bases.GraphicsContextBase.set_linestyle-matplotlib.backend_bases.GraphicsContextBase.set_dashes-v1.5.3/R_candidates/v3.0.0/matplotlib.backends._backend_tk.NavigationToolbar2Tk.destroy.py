    def destroy(self, *args):
        del self.message
        Tk.Frame.destroy(self, *args)
