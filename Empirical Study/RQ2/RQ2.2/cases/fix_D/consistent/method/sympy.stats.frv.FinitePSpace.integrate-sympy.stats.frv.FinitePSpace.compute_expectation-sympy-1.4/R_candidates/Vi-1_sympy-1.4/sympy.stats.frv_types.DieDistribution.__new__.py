    def __new__(cls, sides):
        sides_sym = sympify(sides)
        if fuzzy_not(fuzzy_and((sides_sym.is_integer, sides_sym.is_positive))):
            raise ValueError("'sides' must be a positive integer.")
        else:
            return super(DieDistribution, cls).__new__(cls, sides)
