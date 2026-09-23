    def symbol(self, s, loc, toks):
        # print "symbol", toks
        c = toks[0]
        try:
            char = Char(c, self.get_state())
        except ValueError:
            raise ParseFatalException(s, loc, "Unknown symbol: %s" % c)

        if c in self._spaced_symbols:
            # iterate until we find previous character, needed for cases
            # such as ${ -2}$, $ -2$, or $   -2$.
            for i in six.moves.xrange(1, loc + 1):
                prev_char = s[loc-i]
                if prev_char != ' ':
                    break
            # Binary operators at start of string should not be spaced
            if (c in self._binary_operators and
                    (len(s[:loc].split()) == 0 or prev_char == '{' or
                        prev_char in self._left_delim)):
                return [char]
            else:
                return [Hlist([self._make_space(0.2),
                               char,
                               self._make_space(0.2)] ,
                               do_kern = True)]
        elif c in self._punctuation_symbols:

            # Do not space commas between brackets
            if c == ',':
                prev_char, next_char = '', ''
                for i in six.moves.xrange(1, loc + 1):
                    prev_char = s[loc - i]
                    if prev_char != ' ':
                        break
                for i in six.moves.xrange(1, len(s) - loc):
                    next_char = s[loc + i]
                    if next_char != ' ':
                        break
                if (prev_char == '{' and next_char == '}'):
                    return [char]

            # Do not space dots as decimal separators
            if (c == '.' and s[loc - 1].isdigit() and s[loc + 1].isdigit()):
                return [char]
            else:
                return [Hlist([char,
                               self._make_space(0.2)],
                               do_kern = True)]
        return [char]
