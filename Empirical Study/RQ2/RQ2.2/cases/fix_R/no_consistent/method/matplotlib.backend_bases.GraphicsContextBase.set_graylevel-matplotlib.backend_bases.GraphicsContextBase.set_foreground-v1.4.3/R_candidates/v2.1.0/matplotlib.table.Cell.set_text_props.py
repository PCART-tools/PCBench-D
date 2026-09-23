    def set_text_props(self, **kwargs):
        'update the text properties with kwargs'
        self._text.update(kwargs)
        self.stale = True
