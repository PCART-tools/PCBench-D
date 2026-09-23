    def __init__(self,
                 family = None,
                 style  = None,
                 variant= None,
                 weight = None,
                 stretch= None,
                 size   = None,
                 fname  = None,  # if set, it's a hardcoded filename to use
                 ):
        self._family = _normalize_font_family(rcParams['font.family'])
        self._slant = rcParams['font.style']
        self._variant = rcParams['font.variant']
        self._weight = rcParams['font.weight']
        self._stretch = rcParams['font.stretch']
        self._size = rcParams['font.size']
        self._file = None

        if isinstance(family, str):
            # Treat family as a fontconfig pattern if it is the only
            # parameter provided.
            if (style is None and
                variant is None and
                weight is None and
                stretch is None and
                size is None and
                fname is None):
                self.set_fontconfig_pattern(family)
                return

        self.set_family(family)
        self.set_style(style)
        self.set_variant(variant)
        self.set_weight(weight)
        self.set_stretch(stretch)
        self.set_file(fname)
        self.set_size(size)
