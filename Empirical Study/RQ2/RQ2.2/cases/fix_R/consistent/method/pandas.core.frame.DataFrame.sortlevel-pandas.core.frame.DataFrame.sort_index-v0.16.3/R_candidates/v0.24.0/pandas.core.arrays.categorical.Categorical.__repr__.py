    def __repr__(self):
        # We want PandasObject.__repr__, which dispatches to __unicode__
        return super(ExtensionArray, self).__repr__()
