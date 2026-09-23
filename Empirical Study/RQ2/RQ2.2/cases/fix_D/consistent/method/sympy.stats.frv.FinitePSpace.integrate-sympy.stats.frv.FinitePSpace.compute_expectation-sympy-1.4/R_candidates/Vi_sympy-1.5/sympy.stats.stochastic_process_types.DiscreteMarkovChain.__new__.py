    def __new__(cls, sym, state_space=S.Reals, trans_probs=None):
        sym = _symbol_converter(sym)
        state_space = _set_converter(state_space)
        if trans_probs != None:
            trans_probs = _matrix_checks(trans_probs)
        return Basic.__new__(cls, sym, state_space, trans_probs)
