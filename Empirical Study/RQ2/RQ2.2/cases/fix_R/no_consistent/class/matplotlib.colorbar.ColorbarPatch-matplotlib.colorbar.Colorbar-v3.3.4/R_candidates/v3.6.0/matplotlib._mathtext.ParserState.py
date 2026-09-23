class ParserState:
    """
    Parser state.

    States are pushed and popped from a stack as necessary, and the "current"
    state is always at the top of the stack.

    Upon entering and leaving a group { } or math/non-math, the stack is pushed
    and popped accordingly.
    """

    def __init__(self, fontset, font, font_class, fontsize, dpi):
        self.fontset = fontset
        self._font = font
        self.font_class = font_class
        self.fontsize = fontsize
        self.dpi = dpi

    def copy(self):
        return copy.copy(self)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, name):
        if name in ('rm', 'it', 'bf'):
            self.font_class = name
        self._font = name

    def get_current_underline_thickness(self):
        """Return the underline thickness for this state."""
        return self.fontset.get_underline_thickness(
            self.font, self.fontsize, self.dpi)
