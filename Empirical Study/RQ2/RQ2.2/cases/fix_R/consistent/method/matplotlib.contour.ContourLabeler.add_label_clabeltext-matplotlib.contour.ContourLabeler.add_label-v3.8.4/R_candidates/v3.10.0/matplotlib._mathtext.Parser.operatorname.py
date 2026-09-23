    def operatorname(self, s: str, loc: int, toks: ParseResults) -> T.Any:
        self.push_state()
        state = self.get_state()
        state.font = 'rm'
        hlist_list: list[Node] = []
        # Change the font of Chars, but leave Kerns alone
        name = toks["name"]
        for c in name:
            if isinstance(c, Char):
                c.font = 'rm'
                c._update_metrics()
                hlist_list.append(c)
            elif isinstance(c, str):
                hlist_list.append(Char(c, state))
            else:
                hlist_list.append(c)
        next_char_loc = loc + len(name) + 1
        if isinstance(name, ParseResults):
            next_char_loc += len('operatorname{}')
        next_char = next((c for c in s[next_char_loc:] if c != ' '), '')
        delimiters = self._delims | {'^', '_'}
        if (next_char not in delimiters and
                name not in self._overunder_functions):
            # Add thin space except when followed by parenthesis, bracket, etc.
            hlist_list += [self._make_space(self._space_widths[r'\,'])]
        self.pop_state()
        # if followed by a super/subscript, set flag to true
        # This flag tells subsuper to add space after this operator
        if next_char in {'^', '_'}:
            self._in_subscript_or_superscript = True
        else:
            self._in_subscript_or_superscript = False

        return Hlist(hlist_list)
