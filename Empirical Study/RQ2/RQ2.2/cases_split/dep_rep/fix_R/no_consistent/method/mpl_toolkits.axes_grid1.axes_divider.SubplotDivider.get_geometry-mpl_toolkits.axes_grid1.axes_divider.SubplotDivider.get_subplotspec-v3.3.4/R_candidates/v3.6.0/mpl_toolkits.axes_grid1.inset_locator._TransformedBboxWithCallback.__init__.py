    def __init__(self, *args, callback, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = callback
