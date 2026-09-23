    def __init__(self, c, width, state, always=False, char_class=Char):
        alternatives = state.fontset.get_sized_alternatives_for_symbol(
            state.font, c)

        state = state.copy()
        for fontname, sym in alternatives:
            state.font = fontname
            char = char_class(sym, state)
            if char.width >= width:
                break

        factor = width / char.width
        state.fontsize *= factor
        char = char_class(sym, state)

        super().__init__([char])
        self.width = char.width
