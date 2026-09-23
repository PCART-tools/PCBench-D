    def is_absorbing_chain(self):
        trans_probs = self.transition_probabilities
        return any(self.is_absorbing_state(state) == True
                    for state in range(trans_probs.shape[0]))
