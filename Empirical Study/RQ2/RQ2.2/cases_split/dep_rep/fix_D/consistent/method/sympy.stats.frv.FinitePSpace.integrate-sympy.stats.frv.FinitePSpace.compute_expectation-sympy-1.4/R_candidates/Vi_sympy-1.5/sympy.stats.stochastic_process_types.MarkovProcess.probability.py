    def probability(self, condition, given_condition=None, evaluate=True, **kwargs):
        """
        Handles probability queries for Markov process.

        Parameters
        ==========

        condition: Relational
        given_condition: Relational/And

        Returns
        =======
        Probability
            If the information is not sufficient.
        Expr
            In all other cases.

        Note
        ====
        Any information passed at the time of query overrides
        any information passed at the time of object creation like
        transition probabilities, state space.
        Pass the transition matrix using TransitionMatrixOf,
        generator matrix using GeneratorMatrixOf and state space
        using StochasticStateSpaceOf in given_condition using & or And.
        """
        check, mat, state_space, new_given_condition = \
            self._preprocess(given_condition, evaluate)

        if check:
            return Probability(condition, new_given_condition)

        if isinstance(self, ContinuousMarkovChain):
            trans_probs = self.transition_probabilities(mat)
        elif isinstance(self, DiscreteMarkovChain):
            trans_probs = mat

        if isinstance(condition, Relational):
            rv, states = (list(condition.atoms(RandomIndexedSymbol))[0], condition.as_set())
            if isinstance(new_given_condition, And):
                gcs = new_given_condition.args
            else:
                gcs = (new_given_condition, )
            grvs = new_given_condition.atoms(RandomIndexedSymbol)

            min_key_rv = None
            for grv in grvs:
                if grv.key <= rv.key:
                    min_key_rv = grv
            if min_key_rv == None:
                return Probability(condition)

            prob, gstate = dict(), None
            for gc in gcs:
                if gc.has(min_key_rv):
                    if gc.has(Probability):
                        p, gp = (gc.rhs, gc.lhs) if isinstance(gc.lhs, Probability) \
                                    else (gc.lhs, gc.rhs)
                        gr = gp.args[0]
                        gset = Intersection(gr.as_set(), state_space)
                        gstate = list(gset)[0]
                        prob[gset] = p
                    else:
                        _, gstate = (gc.lhs.key, gc.rhs) if isinstance(gc.lhs, RandomIndexedSymbol) \
                                    else (gc.rhs.key, gc.lhs)

            if any((k not in self.index_set) for k in (rv.key, min_key_rv.key)):
                raise IndexError("The timestamps of the process are not in it's index set.")
            states = Intersection(states, state_space)
            for state in Union(states, FiniteSet(gstate)):
                if Ge(state, mat.shape[0]) == True:
                    raise IndexError("No information is available for (%s, %s) in "
                        "transition probabilities of shape, (%s, %s). "
                        "State space is zero indexed."
                        %(gstate, state, mat.shape[0], mat.shape[1]))
            if prob:
                gstates = Union(*prob.keys())
                if len(gstates) == 1:
                    gstate = list(gstates)[0]
                    gprob = list(prob.values())[0]
                    prob[gstates] = gprob
                elif len(gstates) == len(state_space) - 1:
                    gstate = list(state_space - gstates)[0]
                    gprob = S.One - sum(prob.values())
                    prob[state_space - gstates] = gprob
                else:
                    raise ValueError("Conflicting information.")
            else:
                gprob = S.One

            if min_key_rv == rv:
                return sum([prob[FiniteSet(state)] for state in states])
            if isinstance(self, ContinuousMarkovChain):
                return gprob * sum([trans_probs(rv.key - min_key_rv.key).__getitem__((gstate, state))
                                    for state in states])
            if isinstance(self, DiscreteMarkovChain):
                return gprob * sum([(trans_probs**(rv.key - min_key_rv.key)).__getitem__((gstate, state))
                                    for state in states])

        if isinstance(condition, Not):
            expr = condition.args[0]
            return S.One - self.probability(expr, given_condition, evaluate, **kwargs)

        if isinstance(condition, And):
            compute_later, state2cond, conds = [], dict(), condition.args
            for expr in conds:
                if isinstance(expr, Relational):
                    ris = list(expr.atoms(RandomIndexedSymbol))[0]
                    if state2cond.get(ris, None) is None:
                        state2cond[ris] = S.true
                    state2cond[ris] &= expr
                else:
                    compute_later.append(expr)
            ris = []
            for ri in state2cond:
                ris.append(ri)
                cset = Intersection(state2cond[ri].as_set(), state_space)
                if len(cset) == 0:
                    return S.Zero
                state2cond[ri] = cset.as_relational(ri)
            sorted_ris = sorted(ris, key=lambda ri: ri.key)
            prod = self.probability(state2cond[sorted_ris[0]], given_condition, evaluate, **kwargs)
            for i in range(1, len(sorted_ris)):
                ri, prev_ri = sorted_ris[i], sorted_ris[i-1]
                if not isinstance(state2cond[ri], Eq):
                    raise ValueError("The process is in multiple states at %s, unable to determine the probability."%(ri))
                mat_of = TransitionMatrixOf(self, mat) if isinstance(self, DiscreteMarkovChain) else GeneratorMatrixOf(self, mat)
                prod *= self.probability(state2cond[ri], state2cond[prev_ri]
                                 & mat_of
                                 & StochasticStateSpaceOf(self, state_space),
                                 evaluate, **kwargs)
            for expr in compute_later:
                prod *= self.probability(expr, given_condition, evaluate, **kwargs)
            return prod

        if isinstance(condition, Or):
            return sum([self.probability(expr, given_condition, evaluate, **kwargs)
                        for expr in condition.args])

        raise NotImplementedError("Mechanism for handling (%s, %s) queries hasn't been "
                                "implemented yet."%(expr, condition))
