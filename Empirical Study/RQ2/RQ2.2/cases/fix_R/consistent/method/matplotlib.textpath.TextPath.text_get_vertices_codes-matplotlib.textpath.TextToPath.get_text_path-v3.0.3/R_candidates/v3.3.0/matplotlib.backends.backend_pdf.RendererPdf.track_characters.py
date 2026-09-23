    @cbook.deprecated("3.3")
    def track_characters(self, *args, **kwargs):
        """Keep track of which characters are required from each font."""
        self.file._character_tracker.track(*args, **kwargs)
