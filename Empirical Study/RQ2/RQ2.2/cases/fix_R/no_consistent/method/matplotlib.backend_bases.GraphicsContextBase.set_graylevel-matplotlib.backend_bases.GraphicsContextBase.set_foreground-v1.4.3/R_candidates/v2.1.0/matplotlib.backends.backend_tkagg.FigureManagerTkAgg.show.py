    def show(self):
        """
        this function doesn't segfault but causes the
        PyEval_RestoreThread: NULL state bug on win32
        """
        _focus = windowing.FocusManager()
        if not self._shown:
            def destroy(*args):
                self.window = None
                Gcf.destroy(self._num)
            self.canvas._tkcanvas.bind("<Destroy>", destroy)
            self.window.deiconify()
            # anim.py requires this
            self.window.update()
        else:
            self.canvas.draw_idle()
        # Raise the new window.
        self.canvas.manager.window.attributes('-topmost', 1)
        self.canvas.manager.window.attributes('-topmost', 0)
        self._shown = True
