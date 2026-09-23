    def show(self):
        # show the figure window
        self.window.show()
        # raise the window above others and relase the "above lock"
        self.window.set_keep_above(True)
        self.window.set_keep_above(False)
