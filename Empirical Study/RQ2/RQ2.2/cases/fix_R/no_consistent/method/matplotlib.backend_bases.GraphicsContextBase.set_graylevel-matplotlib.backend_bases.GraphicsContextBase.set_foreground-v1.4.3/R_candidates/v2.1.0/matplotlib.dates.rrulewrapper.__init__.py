    def __init__(self, freq, **kwargs):
        self._construct = kwargs.copy()
        self._construct["freq"] = freq
        self._rrule = rrule(**self._construct)
