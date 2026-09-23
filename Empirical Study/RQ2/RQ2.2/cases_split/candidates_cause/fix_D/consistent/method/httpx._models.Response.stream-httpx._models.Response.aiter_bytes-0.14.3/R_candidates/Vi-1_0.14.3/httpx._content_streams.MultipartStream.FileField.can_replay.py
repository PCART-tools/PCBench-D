        def can_replay(self) -> bool:
            return True if isinstance(self.file, (str, bytes)) else self.file.seekable()
