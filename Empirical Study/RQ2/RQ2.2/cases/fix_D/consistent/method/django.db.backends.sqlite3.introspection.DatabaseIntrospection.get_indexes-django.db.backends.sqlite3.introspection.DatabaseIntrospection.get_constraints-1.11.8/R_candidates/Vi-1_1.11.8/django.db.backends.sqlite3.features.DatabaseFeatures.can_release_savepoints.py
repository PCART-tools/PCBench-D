    @cached_property
    def can_release_savepoints(self):
        return self.uses_savepoints
