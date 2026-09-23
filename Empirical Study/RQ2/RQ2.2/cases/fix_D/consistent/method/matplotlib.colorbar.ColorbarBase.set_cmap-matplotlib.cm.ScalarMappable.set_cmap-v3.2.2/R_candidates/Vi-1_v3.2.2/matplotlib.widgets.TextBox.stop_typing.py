    def stop_typing(self):
        notifysubmit = False
        # Because _notify_submit_users might throw an error in the user's code,
        # we only want to call it once we've already done our cleanup.
        if self.capturekeystrokes:
            # Check for toolmanager handling the keypress
            if self.ax.figure.canvas.manager.key_press_handler_id is not None:
                # since the user is no longer typing,
                # reactivate the standard command keys
                for key in self.params_to_disable:
                    rcParams[key] = self.reset_params[key]
            else:
                toolmanager = self.ax.figure.canvas.manager.toolmanager
                toolmanager.keypresslock.release(self)
            notifysubmit = True
        self.capturekeystrokes = False
        self.cursor.set_visible(False)
        self.ax.figure.canvas.draw()
        if notifysubmit:
            self._notify_submit_observers()
