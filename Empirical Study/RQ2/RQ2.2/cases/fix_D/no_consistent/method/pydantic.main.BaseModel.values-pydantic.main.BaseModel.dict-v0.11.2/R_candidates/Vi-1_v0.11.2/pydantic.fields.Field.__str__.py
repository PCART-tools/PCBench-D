    def __str__(self):
        parts = [self.name, 'type=' + display_as_type(self.type_)]

        if self.required:
            parts.append('required')
        else:
            parts.append(f'default={self.default!r}')

        if self.alt_alias:
            parts.append('alias=' + self.alias)
        return ' '.join(parts)
