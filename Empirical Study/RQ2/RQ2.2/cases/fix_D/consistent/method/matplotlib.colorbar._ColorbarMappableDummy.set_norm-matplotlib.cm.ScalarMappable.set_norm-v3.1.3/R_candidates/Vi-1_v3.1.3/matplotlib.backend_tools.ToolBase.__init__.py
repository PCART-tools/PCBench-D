    def __init__(self, toolmanager, name):
        cbook._warn_external(
            'The new Tool classes introduced in v1.5 are experimental; their '
            'API (including names) will likely change in future versions.')
        self._name = name
        self._toolmanager = toolmanager
        self._figure = None
