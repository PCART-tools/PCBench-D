    def symbol(self, s, loc, toks):
        c = toks[0]
        try:
            char = Char(c, self.get_state())
        except ValueError as err:
            raise ParseFatalException(s, loc,
                                      "Unknown symbol: %s" % c) from err

        if c in self._spaced_symbols:
            # iterate until we find previous character, needed for cases
            # such as ${ -2}$, $ -2$, or $   -2$.
            prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
            # Binary operators at start of string should not be spaced
            if (c in self._binary_operators and
                    (len(s[:loc].split()) == 0 or prev_char == '{' or
                     prev_char in self._left_delim)):
                return [char]
            else:
                return [Hlist([self._make_space(0.2),
                               char,
                               self._make_space(0.2)],
                              do_kern=True)]
        elif c in self._punctuation_symbols:

            # Do not space commas between brackets
            if c == ',':
                prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
                next_char = next((c for c in s[loc + 1:] if c != ' '), '')
                if prev_char == '{' and next_char == '}':
                    return [char]

            # Do not space dots as decimal separators
            if c == '.' and s[loc - 1].isdigit() and s[loc + 1].isdigit():
                return [char]
            else:
                return [Hlist([char, self._make_space(0.2)], do_kern=True)]
        return [char]
