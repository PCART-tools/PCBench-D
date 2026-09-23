    def start_group(self, s, loc, toks):
        self.push_state()
        # Deal with LaTeX-style font tokens
        if toks.get("font"):
            self.get_state().font = toks.get("font")
        return []
