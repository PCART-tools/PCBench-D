    def __getattribute__(self, name):
        if name in ['_text2path', 'flipy', 'height', 'width']:
            return getattr(self._renderer, name)
        else:
            return object.__getattribute__(self, name)
