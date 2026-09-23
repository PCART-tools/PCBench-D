    def operatorname(self, s, loc, toks):
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        hlist_list = []
        # Change the font of Chars, but leave Kerns alone
        for c in toks[0]:
            if isinstance(c, Char):
                c.font = 'rm'
                c._update_metrics()
                hlist_list.append(c)
            elif isinstance(c, str):
                hlist_list.append(Char(c, state))
            else:
                hlist_list.append(c)
        next_char_loc = loc + len(toks[0]) + 1
        if isinstance(toks[0], ParseResults):
            next_char_loc += len('operatorname{}')
        next_char = next((c for c in s[next_char_loc:] if c != ' '), '')
        delimiters = self._left_delim | self._ambi_delim | self._right_delim
        delimiters |= {'^', '_'}
        if (next_char not in delimiters and
                toks[0] not in self._overunder_functions):
            # Add thin space except when followed by parenthesis, bracket, etc.
            hlist_list += [self._make_space(self._space_widths[r'\,'])]
        self.pop_state()
        return Hlist(hlist_list)
