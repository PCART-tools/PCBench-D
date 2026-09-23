    @cbook.deprecated("3.3")
    def merge_used_characters(self, *args, **kwargs):
        self.file._character_tracker.merge(*args, **kwargs)
