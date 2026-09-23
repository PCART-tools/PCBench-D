    @property
    def should_show_dimensions(self):
        return self.show_dimensions is True or (self.show_dimensions == 'truncate' and self.is_truncated)
