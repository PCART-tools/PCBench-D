    def show(self):
        # show the figure window
        self.window.show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            self.window.present()
