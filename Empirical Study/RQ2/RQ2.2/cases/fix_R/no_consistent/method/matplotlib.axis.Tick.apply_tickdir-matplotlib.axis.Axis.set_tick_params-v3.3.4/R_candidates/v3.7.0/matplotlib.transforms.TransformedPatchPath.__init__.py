    def __init__(self, patch):
        """
        Parameters
        ----------
        patch : `~.patches.Patch`
        """
        # Defer to TransformedPath.__init__.
        super().__init__(patch.get_path(), patch.get_transform())
        self._patch = patch
