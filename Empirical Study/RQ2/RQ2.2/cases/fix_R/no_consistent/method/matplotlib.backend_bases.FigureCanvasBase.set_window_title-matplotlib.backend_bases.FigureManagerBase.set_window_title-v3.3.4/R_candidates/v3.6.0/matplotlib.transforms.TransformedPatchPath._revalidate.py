    def _revalidate(self):
        patch_path = self._patch.get_path()
        # Force invalidation if the patch path changed; otherwise, let base
        # class check invalidation.
        if patch_path != self._path:
            self._path = patch_path
            self._transformed_path = None
        super()._revalidate()
