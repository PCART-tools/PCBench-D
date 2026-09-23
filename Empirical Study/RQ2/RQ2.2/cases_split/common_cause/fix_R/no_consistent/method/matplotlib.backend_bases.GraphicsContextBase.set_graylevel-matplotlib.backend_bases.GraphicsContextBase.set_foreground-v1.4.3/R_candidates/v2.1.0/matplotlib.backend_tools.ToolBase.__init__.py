    def __init__(self, toolmanager, name):
        warnings.warn('Treat the new Tool classes introduced in v1.5 as ' +
                      'experimental for now, the API will likely change in ' +
                      'version 2.1, and some tools might change name')
        self._name = name
        self._toolmanager = toolmanager
        self._figure = None
