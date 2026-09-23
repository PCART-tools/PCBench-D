    def show(self):
        # show the figure window
        self.window.show()
        self.canvas.draw()
        if mpl.rcParams["figure.raise_window"]:
            meth_name = {3: "get_window", 4: "get_surface"}[self._gtk_ver]
            if getattr(self.window, meth_name)():
                self.window.present()
            else:
                # If this is called by a callback early during init,
                # self.window (a GtkWindow) may not have an associated
                # low-level GdkWindow (on GTK3) or GdkSurface (on GTK4) yet,
                # and present() would crash.
                _api.warn_external("Cannot raise window yet to be setup")
