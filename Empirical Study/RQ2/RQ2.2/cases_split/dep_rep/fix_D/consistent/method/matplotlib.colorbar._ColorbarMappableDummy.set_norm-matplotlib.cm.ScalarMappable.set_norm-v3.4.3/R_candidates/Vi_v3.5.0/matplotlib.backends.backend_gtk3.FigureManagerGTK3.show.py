    def show(self):
        # show the figure window
        self.window.show()
        self.canvas.draw()
        if mpl.rcParams['figure.raise_window']:
            if self.window.get_window():
                self.window.present()
            else:
                # If this is called by a callback early during init,
                # self.window (a GtkWindow) may not have an associated
                # low-level GdkWindow (self.window.get_window()) yet, and
                # present() would crash.
                _api.warn_external("Cannot raise window yet to be setup")
