    @property
    def defaultFont(self):
        # Lazily evaluated (findfont then caches the result) to avoid including
        # the venv path in the json serialization.
        return {ext: self.findfont(family, fontext=ext)
                for ext, family in self.defaultFamily.items()}
