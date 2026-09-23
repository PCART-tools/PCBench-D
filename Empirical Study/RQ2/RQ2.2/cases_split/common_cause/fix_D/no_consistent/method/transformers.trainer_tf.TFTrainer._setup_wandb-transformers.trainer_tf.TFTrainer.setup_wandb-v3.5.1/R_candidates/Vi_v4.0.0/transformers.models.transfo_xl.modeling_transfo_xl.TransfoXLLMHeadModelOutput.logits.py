    @property
    def logits(self):
        # prediction scores are the output of the adaptive softmax, see
        # the file `modeling_transfo_xl_utilities`. Since the adaptive
        # softmax returns the log softmax value, `self.prediction_scores`
        # are strictly speaking not exactly `logits`, but behave the same
        # way logits do.
        return self.prediction_scores
