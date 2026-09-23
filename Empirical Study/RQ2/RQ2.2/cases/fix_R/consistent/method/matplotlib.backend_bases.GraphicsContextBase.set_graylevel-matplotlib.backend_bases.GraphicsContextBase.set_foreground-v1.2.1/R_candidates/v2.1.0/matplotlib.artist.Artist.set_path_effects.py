    def set_path_effects(self, path_effects):
        """
        set path_effects, which should be a list of instances of
        matplotlib.patheffect._Base class or its derivatives.
        """
        self._path_effects = path_effects
        self.stale = True
