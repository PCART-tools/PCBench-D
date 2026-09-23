    def __init__(self, kl, label=None):
        self._callbacks = cbook.CallbackRegistry(signals=["pchanged"])
        self._remove_method = None
        self._label = label
