    def accepts(self, media_type):
        return any(
            accepted_type.match(media_type)
            for accepted_type in self.accepted_types
        )
