    @partial(normalize_token.register, OrderedDict)
    def normalize_ordered_dict(d):
        return type(d).__name__, normalize_token(list(d.items()))
