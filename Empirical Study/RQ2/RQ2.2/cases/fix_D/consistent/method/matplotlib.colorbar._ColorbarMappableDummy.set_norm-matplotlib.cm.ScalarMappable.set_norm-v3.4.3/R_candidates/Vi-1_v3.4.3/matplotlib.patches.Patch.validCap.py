    @_api.deprecated("3.4")
    @_api.classproperty
    def validCap(cls):
        with _api.suppress_matplotlib_deprecation_warning():
            return mlines.Line2D.validCap
