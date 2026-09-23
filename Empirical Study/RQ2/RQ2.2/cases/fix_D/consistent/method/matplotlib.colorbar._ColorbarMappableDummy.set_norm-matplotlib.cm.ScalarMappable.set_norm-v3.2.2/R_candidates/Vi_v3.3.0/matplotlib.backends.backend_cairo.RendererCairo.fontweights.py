    @cbook.deprecated("3.3")
    @property
    def fontweights(self):
        return {
            100:          cairo.FONT_WEIGHT_NORMAL,
            200:          cairo.FONT_WEIGHT_NORMAL,
            300:          cairo.FONT_WEIGHT_NORMAL,
            400:          cairo.FONT_WEIGHT_NORMAL,
            500:          cairo.FONT_WEIGHT_NORMAL,
            600:          cairo.FONT_WEIGHT_BOLD,
            700:          cairo.FONT_WEIGHT_BOLD,
            800:          cairo.FONT_WEIGHT_BOLD,
            900:          cairo.FONT_WEIGHT_BOLD,
            'ultralight': cairo.FONT_WEIGHT_NORMAL,
            'light':      cairo.FONT_WEIGHT_NORMAL,
            'normal':     cairo.FONT_WEIGHT_NORMAL,
            'medium':     cairo.FONT_WEIGHT_NORMAL,
            'regular':    cairo.FONT_WEIGHT_NORMAL,
            'semibold':   cairo.FONT_WEIGHT_BOLD,
            'bold':       cairo.FONT_WEIGHT_BOLD,
            'heavy':      cairo.FONT_WEIGHT_BOLD,
            'ultrabold':  cairo.FONT_WEIGHT_BOLD,
            'black':      cairo.FONT_WEIGHT_BOLD,
        }
