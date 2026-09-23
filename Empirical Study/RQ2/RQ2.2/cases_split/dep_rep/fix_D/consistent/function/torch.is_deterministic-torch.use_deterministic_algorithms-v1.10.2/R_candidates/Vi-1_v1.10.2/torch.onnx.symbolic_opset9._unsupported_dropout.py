def _unsupported_dropout(name):
    @parse_args("v", "f", "i")
    def feature_dropout(g, input, p, train):
        # NB: In inference mode, FeatureDropout is exported as an identity op.
        if train:
            return _unimplemented(name, "training mode")
        return input
    return feature_dropout
