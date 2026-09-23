    def stop_typing(self):
        notifysubmit = False
        # because _notify_submit_users might throw an error in the
        # user's code, we only want to call it once we've already done
        # our cleanup.
        if self.capturekeystrokes:
            # since the user is no longer typing,
            # reactivate the standard command keys
            for key in self.params_to_disable:
                rcParams[key] = self.reset_params[key]
            notifysubmit = True
        self.capturekeystrokes = False
        self.cursor.set_visible(False)
        self.ax.figure.canvas.draw()
        if notifysubmit:
            self._notify_submit_observers()
