    def get_patch_transform(self):
        if self._patch_type in ('arc', 'circle'):
            self._recompute_transform()
            return self._patch_transform
        else:
            return super().get_patch_transform()
