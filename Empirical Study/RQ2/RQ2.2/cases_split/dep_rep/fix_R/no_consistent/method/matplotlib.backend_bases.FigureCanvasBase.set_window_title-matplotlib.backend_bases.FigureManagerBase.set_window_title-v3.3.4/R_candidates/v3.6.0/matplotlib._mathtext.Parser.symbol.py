    def symbol(self, s, loc, toks):
        c = toks["sym"]
        if c == "-":
            # "U+2212 minus sign is the preferred representation of the unary
            # and binary minus sign rather than the ASCII-derived U+002D
            # hyphen-minus, because minus sign is unambiguous and because it
            # is rendered with a more desirable length, usually longer than a
            # hyphen." (https://www.unicode.org/reports/tr25/)
            c = "\N{MINUS SIGN}"
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
                     prev_char in self._left_delims)):
                return [char]
            else:
                return [Hlist([self._make_space(0.2),
                               char,
                               self._make_space(0.2)],
                              do_kern=True)]
        elif c in self._punctuation_symbols:
            prev_char = next((c for c in s[:loc][::-1] if c != ' '), '')
            next_char = next((c for c in s[loc + 1:] if c != ' '), '')

            # Do not space commas between brackets
            if c == ',':
                if prev_char == '{' and next_char == '}':
                    return [char]

            # Do not space dots as decimal separators
            if c == '.' and prev_char.isdigit() and next_char.isdigit():
                return [char]
            else:
                return [Hlist([char, self._make_space(0.2)], do_kern=True)]
        return [char]
