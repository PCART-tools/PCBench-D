    def __str__(self):
        if self.alt_alias:
            return f"{self.name} (alias '{self.alias}'): " + ', '.join(f'{k}={v!r}' for k, v in self.info.items())
        else:
            return f'{self.name}: ' + ', '.join(f'{k}={v!r}' for k, v in self.info.items())
