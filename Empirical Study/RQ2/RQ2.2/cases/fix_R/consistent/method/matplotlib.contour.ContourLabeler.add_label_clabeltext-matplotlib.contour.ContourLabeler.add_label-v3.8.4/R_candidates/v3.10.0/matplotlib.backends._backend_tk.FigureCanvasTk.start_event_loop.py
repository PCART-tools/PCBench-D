    def start_event_loop(self, timeout=0):
        # docstring inherited
        if timeout > 0:
            milliseconds = int(1000 * timeout)
            if milliseconds > 0:
                self._event_loop_id = self._tkcanvas.after(
                    milliseconds, self.stop_event_loop)
            else:
                self._event_loop_id = self._tkcanvas.after_idle(
                    self.stop_event_loop)
        self._tkcanvas.mainloop()
