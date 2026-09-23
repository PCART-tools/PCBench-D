def is_one_of_factory(legal_values):
    def inner(x):
        from pandas.core.common import pprint_thing as pp
        if not x in legal_values:
            pp_values = lmap(pp, legal_values)
            raise ValueError("Value must be one of %s"
                             % pp("|".join(pp_values)))

    return inner
