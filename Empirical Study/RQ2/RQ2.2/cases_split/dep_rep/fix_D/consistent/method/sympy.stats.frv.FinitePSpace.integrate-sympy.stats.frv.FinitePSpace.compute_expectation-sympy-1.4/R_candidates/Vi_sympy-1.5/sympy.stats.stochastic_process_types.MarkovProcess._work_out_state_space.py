    def _work_out_state_space(self, state_space, given_condition, trans_probs):
        """
        Helper function to extract state space if there
        is a random symbol in the given condition.
        """
        # if given condition is None, then there is no need to work out
        # state_space from random variables
        if given_condition != None:
            rand_var = list(given_condition.atoms(RandomSymbol) -
                        given_condition.atoms(RandomIndexedSymbol))
            if len(rand_var) == 1:
                state_space = rand_var[0].pspace.set
        if not FiniteSet(*[i for i in range(trans_probs.shape[0])]).is_subset(state_space):
            raise ValueError("state space is not compatible with the transition probabilites.")
        state_space = FiniteSet(*[i for i in range(trans_probs.shape[0])])
        return state_space
