    def __init__(self):
        """
        Initialization
        """
        self.mathtext_parser = MathTextParser('path')
        self.tex_font_map = None

        from matplotlib.cbook import maxdict
        self._ps_fontd = maxdict(50)

        self._texmanager = None

        self._adobe_standard_encoding = None
