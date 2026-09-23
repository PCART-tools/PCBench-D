    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        banned_tokens = self._calc_banned_bad_words_ids(input_ids)
        scores = self._set_scores_to_inf_for_banned_tokens(scores, banned_tokens)

        return scores
