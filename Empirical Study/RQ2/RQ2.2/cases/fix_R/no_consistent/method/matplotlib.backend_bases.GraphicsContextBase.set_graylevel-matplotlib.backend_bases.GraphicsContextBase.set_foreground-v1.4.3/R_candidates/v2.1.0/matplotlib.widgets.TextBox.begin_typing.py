    def begin_typing(self, x):
        self.capturekeystrokes = True
        # disable command keys so that the user can type without
        # command keys causing figure to be saved, etc
        self.reset_params = {}
        for key in self.params_to_disable:
            self.reset_params[key] = rcParams[key]
            rcParams[key] = []
