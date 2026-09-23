    def make_rcparams_key(self):
        return [id(fontManager)] + [
            rcParams[param] for param in self.invalidating_rcparams]
