    def get_patch_transform(self):
        return self.patch.get_patch_transform() + self._shadow_transform
