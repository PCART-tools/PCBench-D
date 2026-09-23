    def non_math(self, s, loc, toks):
        s = toks[0].replace(r'\$', '$')
        symbols = [Char(c, self.get_state(), math=False) for c in s]
        hlist = Hlist(symbols)
        # We're going into math now, so set font to 'it'
        self.push_state()
        self.get_state().font = mpl.rcParams['mathtext.default']
        return [hlist]
