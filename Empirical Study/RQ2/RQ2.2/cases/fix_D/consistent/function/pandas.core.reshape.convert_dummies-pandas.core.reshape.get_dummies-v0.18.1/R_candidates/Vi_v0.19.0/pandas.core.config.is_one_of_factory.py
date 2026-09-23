def is_one_of_factory(legal_values):

    callables = [c for c in legal_values if callable(c)]
    legal_values = [c for c in legal_values if not callable(c)]

    def inner(x):
        from pandas.formats.printing import pprint_thing as pp
        if x not in legal_values:

            if not any([c(x) for c in callables]):
                pp_values = pp("|".join(lmap(pp, legal_values)))
                msg = "Value must be one of {0}".format(pp_values)
                if len(callables):
                    msg += " or a callable"
                raise ValueError(msg)

    return inner
