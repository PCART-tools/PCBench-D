    def __init__(self, lines, arrows, **kwargs):
        if kwargs:
            _api.warn_deprecated(
                "3.3",
                message="Passing arbitrary keyword arguments to StreamplotSet "
                        "is deprecated since %(since) and will become an "
                        "error %(removal)s.")
        self.lines = lines
        self.arrows = arrows
