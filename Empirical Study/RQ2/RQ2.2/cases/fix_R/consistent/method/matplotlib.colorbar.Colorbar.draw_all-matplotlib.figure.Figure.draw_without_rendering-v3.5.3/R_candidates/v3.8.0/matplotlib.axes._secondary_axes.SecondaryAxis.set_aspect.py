    def set_aspect(self, *args, **kwargs):
        """
        Secondary axes cannot set the aspect ratio, so calling this just
        sets a warning.
        """
        _api.warn_external("Secondary axes can't set the aspect ratio")
