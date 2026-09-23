    def set_path_effects(self, path_effects):
        """Set the path effects.

        Parameters
        ----------
        path_effects : `.AbstractPathEffect`
        """
        self._path_effects = path_effects
        self.stale = True
