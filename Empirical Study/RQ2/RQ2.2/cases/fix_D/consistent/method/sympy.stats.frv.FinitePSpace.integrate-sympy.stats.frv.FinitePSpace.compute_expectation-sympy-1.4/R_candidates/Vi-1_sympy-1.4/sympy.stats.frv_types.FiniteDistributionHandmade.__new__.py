    def __new__(cls, density):
        density = Dict(density)
        for k in density.values():
            k_sym = sympify(k)
            if fuzzy_not(fuzzy_and((k_sym.is_nonnegative, (k_sym - 1).is_nonpositive))):
                raise ValueError("Probability at a point must be between 0 and 1.")
        sum_sym = sum(density.values())
        if sum_sym != 1:
            raise ValueError("Total Probability must be equal to 1.")
        return Basic.__new__(cls, density)
