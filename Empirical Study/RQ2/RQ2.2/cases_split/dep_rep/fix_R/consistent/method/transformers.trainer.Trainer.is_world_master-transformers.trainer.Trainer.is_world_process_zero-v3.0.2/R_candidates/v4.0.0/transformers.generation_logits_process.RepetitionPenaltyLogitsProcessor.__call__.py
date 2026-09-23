    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        for i in range(scores.shape[0]):
            for previous_token in set(input_ids[i].tolist()):
                # if score < 0 then repetition penalty has to be multiplied to reduce the previous token probability
                if scores[i, previous_token] < 0:
                    scores[i, previous_token] *= self.penalty
                else:
                    scores[i, previous_token] /= self.penalty
        return scores
