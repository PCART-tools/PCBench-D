    def show(self):
        self.window.show()
        if matplotlib.rcParams['figure.raise_window']:
            self.window.activateWindow()
            self.window.raise_()
