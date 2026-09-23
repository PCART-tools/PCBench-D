    def __init__(self, default_font_prop, mathtext_backend):
        """
        *default_font_prop*: A
        :class:`~matplotlib.font_manager.FontProperties` object to use
        for the default non-math font, or the base font for Unicode
        (generic) font rendering.

        *mathtext_backend*: A subclass of :class:`MathTextBackend`
        used to delegate the actual rendering.
        """
        self.default_font_prop = default_font_prop
        self.mathtext_backend = mathtext_backend
        self.used_characters = {}
