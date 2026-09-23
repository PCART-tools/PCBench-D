    def __new__(cls, process, state_space):
        if not isinstance(process, (DiscreteMarkovChain, ContinuousMarkovChain)):
            raise ValueError("Currently only DiscreteMarkovChain and ContinuousMarkovChain "
                                "support StochasticStateSpaceOf.")
        state_space = _set_converter(state_space)
        return Basic.__new__(cls, process, state_space)
