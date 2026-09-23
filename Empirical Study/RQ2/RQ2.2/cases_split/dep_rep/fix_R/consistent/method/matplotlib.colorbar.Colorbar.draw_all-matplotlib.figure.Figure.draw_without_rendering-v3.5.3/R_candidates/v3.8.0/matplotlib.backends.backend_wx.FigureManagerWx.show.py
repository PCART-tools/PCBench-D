    def show(self):
        # docstring inherited
        self.frame.Show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            self.frame.Raise()
