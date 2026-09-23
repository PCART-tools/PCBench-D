    def __new__(cls, sym, process, distribution=None):
        sym = _symbol_converter(sym)
        from sympy.stats.stochastic_process_types import StochasticProcess
        if not isinstance(process, StochasticProcess):
            raise TypeError("`process` must be an instance of StochasticProcess.")
        return Basic.__new__(cls, sym, process, distribution)
