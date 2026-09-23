    def begin_typing(self, x):
        self.capturekeystrokes = True
        # Check for toolmanager handling the keypress
        if self.ax.figure.canvas.manager.key_press_handler_id is not None:
            # disable command keys so that the user can type without
            # command keys causing figure to be saved, etc
            self.reset_params = {}
            for key in self.params_to_disable:
                self.reset_params[key] = rcParams[key]
                rcParams[key] = []
        else:
            self.ax.figure.canvas.manager.toolmanager.keypresslock(self)
