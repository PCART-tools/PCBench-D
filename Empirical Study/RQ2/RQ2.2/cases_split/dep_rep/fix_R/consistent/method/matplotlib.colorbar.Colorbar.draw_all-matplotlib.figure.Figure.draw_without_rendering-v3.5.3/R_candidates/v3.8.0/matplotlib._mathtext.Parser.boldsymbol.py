    def boldsymbol(self, toks: ParseResults) -> T.Any:
        self.push_state()
        state = self.get_state()
        hlist: list[Node] = []
        name = toks["value"]
        for c in name:
            if isinstance(c, Hlist):
                k = c.children[1]
                if isinstance(k, Char):
                    k.font = "bf"
                    k._update_metrics()
                hlist.append(c)
            elif isinstance(c, Char):
                c.font = "bf"
                if (c.c in self._latin_alphabets or
                   c.c[1:] in self._small_greek):
                    c.font = "bfit"
                    c._update_metrics()
                c._update_metrics()
                hlist.append(c)
            else:
                hlist.append(c)
        self.pop_state()

        return Hlist(hlist)
