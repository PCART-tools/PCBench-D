    def __new__(cls, sym, state_space=S.Reals, gen_mat=None):
        sym = _symbol_converter(sym)
        state_space = _set_converter(state_space)
        if gen_mat != None:
            gen_mat = _matrix_checks(gen_mat)
        return Basic.__new__(cls, sym, state_space, gen_mat)
