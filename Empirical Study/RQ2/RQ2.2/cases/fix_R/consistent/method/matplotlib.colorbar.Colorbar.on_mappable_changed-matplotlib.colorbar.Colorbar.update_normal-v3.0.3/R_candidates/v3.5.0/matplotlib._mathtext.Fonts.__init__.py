    def __init__(self, default_font_prop, mathtext_backend):
        """
        Parameters
        ----------
        default_font_prop : `~.font_manager.FontProperties`
            The default non-math font, or the base font for Unicode (generic)
            font rendering.
        mathtext_backend : `MathtextBackend` subclass
            Backend to which rendering is actually delegated.
        """
        self.default_font_prop = default_font_prop
        self.mathtext_backend = mathtext_backend
        self.used_characters = {}
