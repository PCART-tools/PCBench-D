    def show(self):
        with _restore_foreground_window_at_end():
            if not self._shown:
                def destroy(*args):
                    self.window = None
                    Gcf.destroy(self.num)
                self.canvas._tkcanvas.bind("<Destroy>", destroy)
                self.window.deiconify()
            else:
                self.canvas.draw_idle()
            # Raise the new window.
            self.canvas.manager.window.attributes('-topmost', 1)
            self.canvas.manager.window.attributes('-topmost', 0)
            self._shown = True
