    def substack(self, toks: ParseResults) -> T.Any:
        parts = toks["parts"]
        state = self.get_state()
        thickness = state.get_current_underline_thickness()

        hlist = [Hlist(k) for k in parts[0]]
        max_width = max(map(lambda c: c.width, hlist))

        vlist = []
        for sub in hlist:
            cp = HCentered([sub])
            cp.hpack(max_width, 'exactly')
            vlist.append(cp)

        stack = [val
                 for pair in zip(vlist, [Vbox(0, thickness * 2)] * len(vlist))
                 for val in pair]
        del stack[-1]
        vlt = Vlist(stack)
        result = [Hlist([vlt])]
        return result
