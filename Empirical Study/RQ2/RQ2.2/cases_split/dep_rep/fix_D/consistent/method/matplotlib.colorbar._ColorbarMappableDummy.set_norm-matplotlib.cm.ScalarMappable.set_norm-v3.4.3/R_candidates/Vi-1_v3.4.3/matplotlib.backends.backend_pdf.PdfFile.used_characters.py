    @_api.deprecated("3.3")
    @property
    def used_characters(self):
        return self.file._character_tracker.used_characters
