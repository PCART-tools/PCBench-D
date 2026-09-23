    def set_norm(self, norm):
        'set the normalization instance'
        if norm is None:
            norm = colors.Normalize()
        self.norm = norm
        self.changed()
